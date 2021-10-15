import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import IsAdmin, IsStaffOrAuthorOrReadOnly
from api.serializers import (CommentSerializer, GroupSerializer, PetSerializer,
                             PostSerializer, TokenObtainPairSerializer,
                             UserCodeSerializer, UserSerializer)
from pets.models import Pet
from petselection.settings import EMAIL
from posts.models import Comment, Group, Post
from users.models import User, UserCode


class UserCodeViewSet(CreateAPIView):
    serializer_class = UserCodeSerializer
    queryset = UserCode.objects.all()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        code = uuid.uuid4()
        self.send_code(email, code)
        serializer.save(email=email, confirmation_code=code)

    @staticmethod
    def send_code(email, code):
        send_mail(
            f'Код доступа для регистрации на ресурсе PetSelection',
            f'{code}',
            EMAIL,
            [f'{email}'],
            fail_silently=False,
        )


class UserTokenViewSet(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        if not email:
            return Response("Email is required field.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not confirmation_code:
            return Response("Confirmation code is required field.",
                            status=status.HTTP_400_BAD_REQUEST)
        if not UserCode.objects.filter(email=email,
                                       confirmation_code=confirmation_code):
            return Response("Confirmation code for your email isn't valid.",
                            status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email):
            User.objects.create(email=email)
        serializer.is_valid(raise_exception=True)
        UserCode.objects.get(email=email).delete()
        return Response(serializer.validated_data,
                        status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', )

    @action(methods=('patch', 'get'), detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class PetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', '^breed', '^master',)
    permission_classes = (IsAuthenticated,)


class PostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^author', '^title', '^pet', '^text',)
    permission_classes = (IsAuthenticated,)


class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^title', '^description',)
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)

    def get_queryset(self):
        comments = Comment.objects.filter(review=self.get_post())
        return comments

    def get_post(self):
        review = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        return review

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_post())

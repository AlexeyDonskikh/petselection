import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsMaster,
                             IsStaffOrAuthorOrReadOnly)
from api.serializers import (BreedSerializer, CommentSerializer,
                             GroupSerializer, PetListSerializer,
                             PetWriteSerializer, PostSerializer,
                             SpeciesSerializer, TokenObtainPairSerializer,
                             UserCodeSerializer, UserSerializer)
from pets.models import Breed, Pet, Species
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


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'


class SpeciesViewSet(CategoryViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class BreedViewSet(CategoryViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PetListSerializer
        return PetWriteSerializer


class PostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^author', '^title', '^pet', '^text',)
    permission_classes = (IsStaffOrAuthorOrReadOnly,)


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
        comments = Comment.objects.filter(post=self.get_post())
        return comments

    def get_post(self):
        review = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return review

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

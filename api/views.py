import uuid

from django.core.mail import send_mail
from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import (PetSerializer, TokenObtainPairSerializer,
                             UserCodeSerializer)
from pets.models import Pet
from petselection.settings import EMAIL
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


class PetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', '^breed', '^master',)

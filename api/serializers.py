import datetime as dt

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from pets.models import Pet
from users.models import User, UserCode


class UserCodeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = UserCode


class TokenObtainPairSerializer(serializers.Serializer):
    def validate(self, data):
        email = self.context['request'].data.get('email')
        if dt.datetime.now(dt.timezone.utc) - UserCode.objects.get(
                email=email).created >= dt.timedelta(minutes=720):
            raise serializers.ValidationError(
                f"Your verification code is outdated.")
        new_user = User.objects.get(email=email)
        refresh = self.get_token(new_user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'species', 'breed', 'age', 'weight', 'master',
                  'description',)
        model = Pet

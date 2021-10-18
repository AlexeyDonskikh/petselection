import datetime as dt

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from pets.models import Pet
from posts.models import Comment, Group, Post
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('pk', 'first_name', 'last_name', 'username', 'bio', 'role',
                  'email')
        model = User


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'species', 'breed', 'age', 'weight', 'master',
                  'description',)
        model = Pet


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'description',)
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['post', 'text', 'author', 'created']
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        fields = ('title', 'author', 'pet', 'group', 'text', 'pub_date',
                  'comments')
        model = Post

    def create(self, validated_data):
        comments_data = validated_data.pop('comments')
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)
        return post

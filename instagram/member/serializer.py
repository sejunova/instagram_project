from django.contrib.auth import get_user_model
from rest_framework import serializers

# Model에서 User 가져오는게 아니다.
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'img_profile', 'age', 'nickname')
        read_only_fields = ('password',)


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nickname', 'age')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password should match')
        return data

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password2'],
            age=validated_data['age'],
            nickname=validated_data['nickname']
        )
    # def get_token(self, obj):
    #     return Token.objects.create(user=obj).key

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        data = {
            'user':ret,
            'token':instance.token,
        }
        return data
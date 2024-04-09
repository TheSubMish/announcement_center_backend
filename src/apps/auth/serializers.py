from rest_framework import serializers
from src.apps.auth.models import User

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name' 'username', 'email', 'password')

    def create(self, validated_data):
        first_name = validated_data.get('first_name',None)
        last_name = validated_data.get('last_name',None)
        username = validated_data.get('username',None)
        email = validated_data.get('email',None)
        password = validated_data.get('password',None)

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
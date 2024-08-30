from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from dadata import Dadata


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")

        dadata = Dadata(settings.DADATA_API_KEY, settings.DADATA_SECRET_KEY)
        result = dadata.clean('email', value)

        if (result['qc'] != 0) and (result['type'] == 'DISPOSABLE'):
            raise serializers.ValidationError('Некорректный или временный email')

        return value

    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            password=validate_data['password'],
        )
        return user

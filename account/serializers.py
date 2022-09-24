from rest_framework import serializers

from .models import User
from .authentications import jwt_encode

from django.contrib.auth.hashers import make_password
from datetime import datetime

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password'
        ]

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        attrs['password'] = make_password(attrs.get('password'))
        return attrs

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password')
        return ret


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def login(self):
        try:
            user = User.objects.get(email=self.data.get('email'))
        except:
            raise serializers.ValidationError({'detail':'Incorrect authentication credentials.'})
        if not user.check_password(self.data.get('password')):
            raise serializers.ValidationError({'detail':'Incorrect authentication credentials.'})
        if not user.is_active:
            raise serializers.ValidationError({'detail':'Inactive user.'})
        user.last_login = datetime.now()
        user.save()
        token = jwt_encode(
            {
                'uuid': str(user.uuid),
                'email': user.email
            }
        )
        self.token = token


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_active',
        ]

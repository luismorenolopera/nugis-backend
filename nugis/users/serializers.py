from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Public user fields only. Permission flags are never writable."""

    password = serializers.CharField(write_only=True, min_length=8,
                                     style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'password', 'date_joined')
        read_only_fields = ('id', 'date_joined')

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            candidate = User(**{k: v for k, v in attrs.items() if k != 'password'})
            validate_password(password, user=candidate)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

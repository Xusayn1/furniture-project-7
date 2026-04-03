import re

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from products.models import Product
from blogs.models import Post

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_premium = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'full_name',
            'phone_number',
            'is_premium',
        ]
        read_only_fields = ('id', 'email', 'is_premium')

    def get_is_premium(self, obj):
        profile = getattr(obj, 'profile', None)
        return getattr(profile, 'is_premium', False)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'full_name', 'phone_number', 'password')
        read_only_fields = ('id',)

    def validate(self, attrs):
        password = attrs.get('password', '')
        rules = [
            (len(password) >= 8, "at least 8 characters"),
            (re.search(r"[A-Z]", password), "one uppercase letter"),
            (re.search(r"\d", password), "one digit"),
            (re.search(r"[!@#$%^&*]", password), "one special character (!@#$%^&*)"),
        ]
        missing = [msg for ok, msg in rules if not ok]
        if missing:
            msg = "Password must contain " + ", ".join(missing) + "."
            raise serializers.ValidationError({"password": msg})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        try:
            user = User.objects.get(Q(username__iexact=identifier) | Q(email__iexact=identifier))
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials")

        user_in = authenticate(self.context.get('request'), email=user.email, password=password)
        if user_in is None:
            raise AuthenticationFailed("Invalid credentials")

        attrs['user'] = user_in
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs.get('refresh')
        if not refresh:
            raise serializers.ValidationError({"refresh": "Refresh token is required"})
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'featured', 'author', 'created_at', 'updated_at']
        read_only_fields = ('id', 'author', 'featured', 'created_at', 'updated_at')

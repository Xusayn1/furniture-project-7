from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework import serializers

from products.models import Product

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')
        try:
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found, please check your credentials")

        credentials = {'email': user.email, 'password': password}

        user_in = authenticate(self.context.get('request'), **credentials)
        if user_in is None:
            raise serializers.ValidationError("User not found, please check your credentials")

        attrs['user'] = user_in
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']
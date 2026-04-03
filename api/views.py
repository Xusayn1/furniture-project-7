from django.apps import apps
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsOwnerOrReadOnly, IsPremiumUser
from api.serializers import (
    LoginSerializer,
    LogoutSerializer,
    ProductSerializer,
    RegisterSerializer,
    UserSerializer,
)
from products.models import Product


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        data = {
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as exc:
            raise InvalidToken(detail="Invalid or expired refresh token") from exc

        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        data = self.serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Post CRUD with owner/admin protection.
    Anonymous: read-only
    Authenticated: read + create
    Owner/Admin: full access on their objects
    """

    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        Post = apps.get_model('blogs', 'Post')
        return Post.objects.all()

    def get_serializer_class(self):
        from api.serializers import PostSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsPremiumUser],
        url_path="feature",
    )
    def feature(self, request, pk=None):
        post = self.get_object()
        post.featured = True
        post.save(update_fields=["featured", "updated_at"] if hasattr(post, "updated_at") else ["featured"])
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

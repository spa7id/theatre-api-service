from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    pagination_class = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

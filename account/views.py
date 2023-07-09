from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from account.serializers import RegisterSerializer


class RegisterViewSet(GenericViewSet, mixins.CreateModelMixin):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

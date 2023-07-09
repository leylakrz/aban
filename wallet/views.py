from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wallet.models import Wallet
from wallet.serializers import WalletSerializer, WalletChargeSerializer


class WalletViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = WalletSerializer

    def get_serializer_class(self):
        if self.action == "charge":
            return WalletChargeSerializer
        return WalletSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_queryset(self):
        return Wallet.objects.filter(user_id=self.request.user.id)

    @action(detail=False, methods=["put"], name="charge")
    def charge(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
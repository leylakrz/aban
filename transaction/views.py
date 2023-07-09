from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import GenericViewSet

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class TransactionViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = Transaction.objects
        if self.action == "list":
            return qs.filter(user=self.request.user)
        else:
            return qs.all()

    def get_serializer_context(self):
        return {"user": self.request.user}

    @action(detail=False, methods=["post"], name="buy")
    def buy(self, request, *args, **kwargs):
        return super(TransactionViewSet, self).create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        raise NotFound

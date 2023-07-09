from django.db.models import F, Subquery
from rest_framework import serializers

from cryptocurrency.models import Cryptocurrency
from wallet.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    cryptocurrency = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ["cryptocurrency", "balance"]

    def get_cryptocurrency(self, obj):
        return obj.cryptocurrency.name


class WalletChargeSerializer(WalletSerializer):
    class Meta:
        model = Wallet
        fields = ["balance"]

    def create(self, validated_data):
        cryptocurrency_id = Subquery(Cryptocurrency.objects.filter(name="RIAL").values('id')[:1])
        wallet_obj, created = Wallet.objects.get_or_create(user=self.context.get("user"),
                                                           cryptocurrency_id=cryptocurrency_id)
        wallet_obj.balance = F("balance") + validated_data["balance"]
        wallet_obj.save()
        return wallet_obj

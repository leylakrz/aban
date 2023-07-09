import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from cryptocurrency.models import Cryptocurrency
from transaction.models import Transaction
from utils.exceptions import ServerError
from utils.exchange_utils import ExchangeHandler


class TransactionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    cryptocurrency = serializers.CharField()

    class Meta:
        model = Transaction
        exclude = ("user",)
        extra_kwargs = {"total_price": {"read_only": True}}

    def get_status(self, obj):
        return Transaction.TransactionStatusChoices(str(obj.status)).label

    def create(self, validated_data):
        cryptocurrency_obj = get_object_or_404(Cryptocurrency, name=validated_data["cryptocurrency"])
        validated_data["total_price"] = cryptocurrency_obj.current_price * validated_data["number"]
        with ExchangeHandler() as exchange_handler:  # handles redis lock
            try:
                successful = exchange_handler.handle_buy_from_exchange(validated_data["total_price"],
                                                                       validated_data["cryptocurrency"],
                                                                       validated_data["number"], )
                if successful:
                    validated_data["status"] = Transaction.TransactionStatusChoices.DONE.value
            except Exception as error:
                logging.exception(error)
                raise ServerError

            validated_data["user"] = self.context["user"]
            validated_data["cryptocurrency"] = cryptocurrency_obj
            obj = super(TransactionSerializer, self).create(validated_data)
            if not successful:
                exchange_handler.add_pending_transaction(obj.id)
            return obj

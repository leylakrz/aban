from django.core.cache import cache

from aban.settings import EXCHANGE_MINIMUM_PRICE
from transaction.models import Transaction
from utils.redis_utils import EXCHANGE_PRICE_KEY, PENDING_TRANSACTION_IDS_KEY, CacheLockHandler


def buy_from_exchange(cryptocurrency_name, cryptocurrency_num):
    return True


class ExchangeHandler(CacheLockHandler):
    @staticmethod
    def handle_buy_from_exchange(new_total_price, cryptocurrency_name, cryptocurrency_num):
        exchange_price_cached = cache.get(EXCHANGE_PRICE_KEY, 0)
        exchange_price = exchange_price_cached + new_total_price
        if exchange_price >= EXCHANGE_MINIMUM_PRICE:
            successful = buy_from_exchange(cryptocurrency_name, cryptocurrency_num)
            if successful and exchange_price_cached:
                redis_conn = cache.client.get_client(write=True)
                pending_transaction_ids = redis_conn.lrange(PENDING_TRANSACTION_IDS_KEY, 0, -1)
                Transaction.objects.set_as_done(pending_transaction_ids)
                cache.delete(EXCHANGE_PRICE_KEY)
                redis_conn.delete(PENDING_TRANSACTION_IDS_KEY)
            return True

        cache.set(EXCHANGE_PRICE_KEY, exchange_price)
        return False

    @staticmethod
    def add_pending_transaction(transaction_id):
        cache.client.get_client(write=True).rpush(PENDING_TRANSACTION_IDS_KEY, transaction_id)

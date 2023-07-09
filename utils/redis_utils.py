import time

from django.core.cache import cache

EXCHANGE_LOCK = "EXC"
EXCHANGE_PRICE_KEY = "EXC_PR"
PENDING_TRANSACTION_IDS_KEY = "PEND_TRA"



class CacheLockHandler:
    cache_client = cache
    lock_id = EXCHANGE_LOCK

    def __init__(self):
        self.acquired_lock = cache.lock(self.lock_id)

    def __enter__(self):
        self.acquire_lock()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release_lock()

    def acquire_lock(self):
        while True:
            self.acquired_lock = cache.lock(self.lock_id)
            if self.acquired_lock.acquire(blocking=False):
                break
            else:
                time.sleep(0.1)  # the same default time as django_redis

    def release_lock(self):
        if self.acquired_lock:
            self.acquired_lock.release()

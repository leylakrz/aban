from unittest.mock import patch

import redis
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.test import override_settings
from rest_framework.test import APIRequestFactory, force_authenticate

from aban import settings
from .models import Transaction, Cryptocurrency
from .views import TransactionViewSet


def cache_mocker(func):
    def wrapper(*args, **kwargs):
        with override_settings(CACHES={"default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:6379/12",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }}):  # tried mock backends,
            # lock was not implemented
            return func(*args, **kwargs)

    return wrapper


class TransactionViewSetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()
        cls.client = Client()
        cls.user = User.objects.create(username='testuser')
        cls.access_token = cls.login_user()
        cls.cryptocurrency_name = "TEST"
        Cryptocurrency.objects.create(name=cls.cryptocurrency_name, current_price=100)

    @classmethod
    def tearDownClass(cls):
        cls.clear_redis_database()
        super().tearDownClass()

    @classmethod
    def clear_redis_database(cls):
        redis_url = settings.CACHES['default']['LOCATION']
        connection = redis.from_url(redis_url)
        connection.flushdb()

    @classmethod
    def login_user(cls):
        response = cls.client.post('/account/token/', {'username': 'testuser', 'password': 'testpass'},
                                   content_type='application/json')
        return response.json().get('access_token')

    def create_transaction(self, data):
        request = self.factory.post('/transaction/buy/', data=data, format='json')
        request.user = self.user
        force_authenticate(request, user=self.user, token=self.access_token)
        view = TransactionViewSet.as_view({'post': 'buy'})
        response = view(request)
        return response

    @cache_mocker
    @patch('utils.exchange_utils.buy_from_exchange', return_value=True)
    def test_buy_successful(self, mock_handle_buy):
        data = {
            "cryptocurrency": self.cryptocurrency_name,
            "number": 10
        }
        response = self.create_transaction(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.cryptocurrency.name, self.cryptocurrency_name)
        self.assertEqual(transaction.total_price, 1000)
        self.assertEqual(str(transaction.status), Transaction.TransactionStatusChoices.DONE.value)

    @cache_mocker
    @patch('utils.exchange_utils.ExchangeHandler.handle_buy_from_exchange', return_value=False)
    def test_buy_pending(self, mock_handle_buy):
        data = {
            "cryptocurrency": self.cryptocurrency_name,
            "number": 1
        }
        response = self.create_transaction(data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.cryptocurrency.name, self.cryptocurrency_name)
        self.assertEqual(transaction.total_price, 100)
        self.assertEqual(str(transaction.status), Transaction.TransactionStatusChoices.PENDING.value)

    @cache_mocker
    @patch('utils.exchange_utils.ExchangeHandler.handle_buy_from_exchange')
    def test_buy_exception(self, mock_handle_buy):
        mock_handle_buy.side_effect = Exception("Some error")

        data = {
            "cryptocurrency": self.cryptocurrency_name,
            "number": 10
        }
        response = self.create_transaction(data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(Transaction.objects.count(), 0)

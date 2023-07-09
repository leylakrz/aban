from django.contrib.auth.models import User
from django.db import models
from django.db.models import TextChoices

from cryptocurrency.models import Cryptocurrency
from transaction.managers import TransactionManager


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    number = models.IntegerField()  # could be float?
    total_price = models.FloatField()

    class TransactionStatusChoices(TextChoices):
        PENDING = 0, "در حال بررسی"
        DONE = 1, "موفق"
        FAILED = 2, "ناموفق"

    status = models.IntegerField(choices=TransactionStatusChoices.choices,
                                 default=TransactionStatusChoices.PENDING.value)

    objects = TransactionManager()

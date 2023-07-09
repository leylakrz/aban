from django.contrib.auth.models import User
from django.db import models

from cryptocurrency.models import Cryptocurrency


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

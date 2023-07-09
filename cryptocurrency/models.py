from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    current_price = models.FloatField(default=4)

    def __str__(self):
        return self.name

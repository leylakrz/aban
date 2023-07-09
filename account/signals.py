from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from cryptocurrency.models import Cryptocurrency
from wallet.models import Wallet, WalletCryptocurrency


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        rial_cryptocurrency_obj, _ = Cryptocurrency.objects.get_or_create(name="RIAL")
        wallet_obj = Wallet.objects.create(user=instance)
        WalletCryptocurrency.objects.create(wallet_id=wallet_obj.id,
                                            cryptocurrency_id=rial_cryptocurrency_obj.id)

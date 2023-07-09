from django.db.models.manager import Manager


class TransactionManager(Manager):
    def set_as_done(self, transaction_ids):
        self.filter(id__in=transaction_ids).update(status=self.model.TransactionStatusChoices.DONE.value)

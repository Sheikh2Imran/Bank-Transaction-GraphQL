from django.db import models
from django.utils import timezone

from account.models import Account


class Transaction(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    pay_for = models.CharField(max_length=20, default='Pekhom')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bank_ac_number = models.CharField(max_length=25)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "pay_for: {} || bank account number: {}".format(self.pay_for, self.bank_ac_number)
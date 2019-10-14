from django.db import models
from django.conf import settings


class Account(models.Model):
    username = models.CharField(max_length=50)
    identifier = models.CharField(max_length=20)
    circuit_id = models.CharField(max_length=10)
    connect_id = models.CharField(max_length=32)
    mobile_number = models.CharField(max_length=15)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "username: {} || connect_id: {}".format(self.username, self.connect_id)
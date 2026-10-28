from django.db import models


class Banking(models.Model):
    account_no = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(max_length=100)

    # Stores a hashed password, not the original password
    password = models.CharField(max_length=128)

    mobile = models.CharField(max_length=15)

    address = models.CharField(max_length=200)

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.account_no} - {self.name}"
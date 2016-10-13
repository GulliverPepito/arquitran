# import moneyed
import uuid
from djmoney.models.fields import MoneyField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class KreditCard(models.Model):
    first_name = models.CharField(
        "Kredit card holder's first name",
        max_length=255,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        "Kredit card holder's last name",
        max_length=255,
        blank=False,
        null=False,
    )

    card_number = models.UUIDField(
        "Unique card number",
        primary_key=True,
        unique=True,
        max_length=255,
        editable=False,
        blank=False,
        null=False,
        default=uuid.uuid4,
    )

    balance = MoneyField(
        "Current available money",
        max_digits=10,
        decimal_places=2,
        default_currency="CLP",
        default=0,
    )

    card_cvv = models.IntegerField(
        "Confirmation code (CVV)",
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(999),
            MinValueValidator(100),
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return " ".join([self.first_name, self.last_name])


class ApplicationToken(models.Model):
    application = models.CharField(
        "Registered application",
        unique=True,
        max_length=255,
        blank=False,
        null=False,
    )

    token = models.UUIDField(
        "Registered application",
        primary_key=True,
        editable=False,
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        default=uuid.uuid4,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.application


class Transaction(models.Model):
    WAITING = 'WAIT'
    EXECUTED = 'EXEC'
    ERRORED = 'ERR'

    id = models.UUIDField(
        "Transaction unique identifier",
        primary_key=True,
        editable=False,
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        default=uuid.uuid4,
    )

    app = models.ForeignKey(
        ApplicationToken,
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(
        KreditCard,
        related_name='sender',
        blank=False,
        null=False,
    )
    recipient = models.ForeignKey(
        KreditCard,
        related_name='recipient',
        blank=False,
        null=False,
    )

    amount = MoneyField(
        "Money to exchange",
        max_digits=10,
        decimal_places=2,
        default_currency="CLP",
        default=0,
    )

    status = models.CharField(
        "Current transaction status code.",
        max_length=4,
        choices=(
            (WAITING, WAITING),
            (EXECUTED, EXECUTED),
            (ERRORED, ERRORED),
        ),
        default=WAITING,
    )

    status_description = models.TextField(
        "Description related to the status.",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "{} -> {} ({})".format(self.sender, self.recipient, self.amount)

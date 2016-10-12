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

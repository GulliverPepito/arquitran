import uuid
from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField

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


class TransactionManager(models.Manager):
    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.kredit_card.balance -= self.amount
            self.kredit_card.save()
            super(TransactionManager, self).save(*args, **kwargs)


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
        editable=False,
        blank=True,
        null=True,
    )

    kredit_card = models.ForeignKey(
        KreditCard,
        editable=False,
        blank=False,
        null=False,
    )

    amount = MoneyField(
        "Money to exchange",
        editable=False,
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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.kredit_card.balance -= self.amount
            self.kredit_card.save()
            super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.kredit_card, self.amount)

import json
import uuid
from django.test import TestCase
from django.test.client import Client
from .models import KreditCard, ApplicationToken

# Create your tests here.


def POST(client, path, data):
    return client.post(path, json.dumps(data),
                       content_type="application/json",
                       follow=True,
                       )


class TransactionTest(TestCase):
    def setUp(self):
        # HTTP request factory
        self.client = Client()

        # Fixatures
        self.kredit_card = KreditCard.objects.create(
            first_name="Patricio",
            last_name="Lopez",
            card_cvv=666,
        )
        self.app = ApplicationToken.objects.create(
            application="alquitran-test"
        )

    def test_invalid_token(self):
        not_registed_payload = {
            "application_token": str(uuid.uuid4()),  # Random token
        }
        response = POST(self.client, "/transactions/", not_registed_payload)
        self.assertEqual(response.status_code, 403)

        blank_payload = {
            "application_token": "",
        }
        response = POST(self.client, "/transactions/", blank_payload)
        self.assertEqual(response.status_code, 403)

        empty_payload = {}
        response = POST(self.client, "/transactions/", empty_payload)
        self.assertEqual(response.status_code, 403)

    def test_valid_transaction(self):
        payload = {
            "application_token": str(self.app.token),
            "kredit_card": {
                "card_number": str(self.kredit_card.card_number),
                "card_cvv": int(self.kredit_card.card_cvv),
                "card_holder": {
                    "first_name": str(self.kredit_card.first_name),
                    "last_name": str(self.kredit_card.last_name),
                },
            },
            "to_charge": {
                "currency": "CLP",
                "amount": 5533
            },
            # "transaction_validation": {
            #     "href": "/transactions/{id}",
            #     "method": "patch"
            # },
        }
        response = POST(self.client, "/transactions/", payload)
        self.assertEqual(response.status_code, 201)

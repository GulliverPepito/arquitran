import json
from moneyed import Money
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import Transaction, KreditCard, ApplicationToken

# Create your views here.


def BAD_REQUEST(msg="Bad request."):
    return HttpResponse(msg, status=400)


def FORBIDDEN(msg="Forbidden. Invalid application token."):
    return HttpResponse(msg, status=403)


def SERVER_ERROR(msg="Server error. Try again :)"):
    return HttpResponse(msg, status=501)


def root(request):
    return render(request, 'index.html')


def create_transaction(request):
    if request.method != 'POST':
        return BAD_REQUEST()

    data = json.loads(request.body.decode("utf-8"))

    try:
        application_token = data['application_token']
        app = ApplicationToken.objects.get(token=application_token)
    except:
        return FORBIDDEN()

    try:
        kredit_card = data["kredit_card"]
        to_charge = data["to_charge"]
    except:
        return BAD_REQUEST()

    try:
        card_holder = kredit_card["card_holder"]
        kard = KreditCard.objects.get(
            card_number=str(kredit_card["card_number"]),
            card_cvv=int(kredit_card["card_cvv"]),
            first_name=str(card_holder["first_name"]),
            last_name=str(card_holder["last_name"]),
        )
        transaction = Transaction.objects.create(
            app=app,
            kredit_card=kard,
            amount=Money(int(to_charge["amount"]), to_charge["currency"]),
            status=Transaction.EXECUTED,
            status_description="Transaction validated and executed",
        )
    except:
        status = {
            "transaction_status_code": "REJ",
            "description": "Transaction rejected. Card details do not match."
        }
        return JsonResponse({"status": status}, status=401)

    transaction.save()
    status = {
        "transaction_status_code": transaction.status,
        "description": transaction.status_description,
    }
    response = JsonResponse({"status": status}, status=201)
    response["Location"] = "/transactions/{}/".format(transaction.id)
    return response


def transaction_status(request, id):
    if request.method != 'GET':
        return BAD_REQUEST()

    try:
        application_token = request.GET['application_token']
        ApplicationToken.objects.get(token=application_token)
        transaction = Transaction.objects.get(id=id)
        amount = transaction.amount
    except:
        return BAD_REQUEST()

    return JsonResponse({
        "to_charge": {
            "currency": str(amount.currency),
            "amount": float(amount.amount),
        },
        "status": {
            "transaction_status_code": transaction.status,
            "description": transaction.status_description,
        }
    })

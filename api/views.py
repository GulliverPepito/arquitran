from django.http import JsonResponse, HttpResponse
from .models import Transaction, KreditCard, ApplicationToken
# from django.shortcuts import render
# from django.views import View

# Create your views here.


def BAD_REQUEST():
    return HttpResponse('Bad request.', status=400)


def FORBIDDEN():
    return HttpResponse('Forbidden. Invalid application token.', status=403)


def SERVER_ERROR():
    return HttpResponse('Server error. Try again :)', status=501)


def create_transaction(request):
    if request.method != 'POST':
        return BAD_REQUEST()

    return HttpResponse('Hello, World!')


def transaction_status(request, id):
    if request.method != 'GET':
        return BAD_REQUEST()

    application_token = request.GET.get('application_token', '')
    if not application_token or application_token == '':
        return FORBIDDEN()

    try:
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

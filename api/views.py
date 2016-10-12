from django.http import HttpResponse
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
    if application_token == '':
        return FORBIDDEN()

    # if not found: 400 Bad request.

    return HttpResponse('Hello, World 111!' + id + application_token)

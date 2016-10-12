from django.http import HttpResponse
# from django.shortcuts import render
# from django.views import View

# Create your views here.


def create_transaction(request):
    # TODO: validate POST
    return HttpResponse('Hello, World!')


def transaction_status(request, id):
    # TODO: validate POST
    return HttpResponse('Hello, World 111!' + id)

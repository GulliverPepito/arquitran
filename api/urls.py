from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^transactions/$', views.create_transaction),
    url(r'^transactions/(?P<id>.*)\/$', views.transaction_status),
]

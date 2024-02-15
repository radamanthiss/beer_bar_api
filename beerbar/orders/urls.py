from django.urls import path
from .views import BeerListAvailable, OrderReceive, GetAccounting, PayOrder


urlpatterns = [
  path("beers/", BeerListAvailable.as_view(), name="list-beers"),
  path("order/", OrderReceive.as_view(), name="receive-order"),
  path("account/", GetAccounting.as_view(), name="get-account"),
  path("pay/", PayOrder.as_view(), name="pay-order"),
]

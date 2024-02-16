from unittest import mock
from django.test import TestCase, RequestFactory
from rest_framework import status

from .models import Beer, Order
from .views import BeerListAvailable, GetAccounting, OrderReceive

class BeerListAvailableTests(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.view = BeerListAvailable.as_view()
    self 
    self.uri = '/api/beers/'

    self.beers = [
        Beer(1, 'IPA', 5.0),
        Beer(2, 'Stout', 6.0),
        Beer(3, 'Pale Ale', 5.5),
    ]
    
    self.orders = []

  def test_list_beers(self):
    request = self.factory.get(self.uri)
    with mock.patch('orders.views.beers', new=self.beers):
      response = self.view(request)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    expected_response_data = [{'id': beer.id, 'name': beer.name, 'price': beer.price, 'is_available': beer.is_available} for beer in self.beers]
    self.assertEqual(response.data, expected_response_data)
    
class OrderReceiveTests(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.view = OrderReceive.as_view()
    self.uri = '/api/order/'
    self.beers = [
      Beer(1, 'IPA', 5.0, True),
      Beer(2, 'Stout', 6.0, False),
    ]
    self.orders = []
    
  def test_order_receive_success(self):
    data = {'beer_id': 1, 'friend_name': 'Kevin', 'quantity': 1}
    request = self.factory.post(self.uri, data, format='json')
    
    with mock.patch('orders.views.beers', new=self.beers), \
          mock.patch('orders.views.orders', new=self.orders):
        response = self.view(request)
    
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(self.orders), 1)
    self.assertEqual(self.orders[0].beer_id, data['beer_id'])

  def test_order_receive_fail_beer_not_available(self):
    data = {'beer_id': 2, 'friend_name': 'Kevin', 'quantity': 1}
    request = self.factory.post(self.uri, data, format='json')
    
    with mock.patch('orders.views.beers', new=self.beers), \
          mock.patch('orders.views.orders', new=self.orders):
        response = self.view(request)
    
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('Beer not available', response.data['message'])
    self.assertEqual(len(self.orders), 0)  # Ensure no orders were added
    
    
class GetAccountingTests(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.view = GetAccounting.as_view()
    self.uri = '/api/account/'
    self.beers = [
      Beer(1, 'IPA', 5.0, True),
      Beer(2, 'Stout', 6.0, True),
      Beer(3, 'Pale Ale', 5.5, True),
    ]
    self.orders = [
      Order('Kevin', 1, 2),
      Order('Sergio', 2, 1),
      Order('Camilo', 3, 1),
    ]
    
  def test_get_total_for_friend(self):
    with mock.patch('orders.views.beers', new=self.beers), \
          mock.patch('orders.views.orders', new=self.orders):
        request = self.factory.get(self.uri, {'friend_name': 'Sergio'})
        response = self.view(request)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    expected_total_value = (self.beers[1].price * 1)
    self.assertEqual(response.data, {'friend_name': 'Sergio', 'total_value': expected_total_value})

  def test_get_total_account(self):
    with mock.patch('orders.views.beers', new=self.beers), \
        mock.patch('orders.views.orders', new=self.orders):
      request = self.factory.get(self.uri)
      response = self.view(request)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    expected_total_value = sum(beer.price * order.quantity for order in self.orders for beer in self.beers if order.beer_id == beer.id)
    self.assertEqual(response.data, {'total_value': expected_total_value})
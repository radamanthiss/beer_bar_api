from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BeerSerializer, OrderSerializer
from .models import Beer, Order


# define a list of beers for the bar
beers = [
    Beer(1, 'IPA', 5.0),
    Beer(2, 'Stout', 6.0),
    Beer(3, 'Pale Ale', 5.5),
    Beer(4, 'Sour', 7.0),
    Beer(5, 'Pilsner', 4.5),
    Beer(6, 'Lager', 4.5)
]

orders = []

class BeerListAvailable(APIView):
  def get(self, request):
    serializer = BeerSerializer(beers, many=True)
    return Response(serializer.data)

class OrderReceive(APIView):
  def post(self, request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
      order_data = serializer.validated_data
      beer_id = order_data['beer_id']
      ordered_beer = next((beer for beer in beers if beer.id == beer_id), None)
      if ordered_beer and ordered_beer.is_available:
        orders.append(Order(**order_data))
        return Response({'message': 'Order received'}, status=201)
      else:
        return Response({'message': 'Beer not available'}, status=400)
    return Response(serializer.errors, status=400)
  

class GetAccounting(APIView):
  def get(self, request):
    total_value = sum(beer.price * order.quantity for order in orders for beer in beers if order.beer_id == beer.id)
    return Response({'total': total_value})

class PayOrder(APIView):
  def post(self, request):
    payment_type = request.data.get('payment_type', 'equal')
    if payment_type == 'equal':
      total_value = sum(beer.price * order.quantity for order in orders for beer in beers if order.beer_id == beer.id)
      value_per_friend = total_value / 3
      return Response({'value_per_friend': value_per_friend})
    elif payment_type == 'individual':
      bill = {order.friend_name: 0 for order in orders}
      for order in orders:
        for beer in beers:
          if order.beer_id == beer.id:
            bill[order.friend_name] += order.quantity * beer.price
      return Response(bill)
    else:
      return Response({'message': 'Invalid payment type'}, status=400)
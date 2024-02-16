from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BeerSerializer, OrderSerializer
from .models import Beer, Order


# define a list of beers for the bar
beers = [
    Beer(1, 'IPA', 5.0, True),
    Beer(2, 'Stout', 6.0,True),
    Beer(3, 'Pale Ale', 5.5,True),
    Beer(4, 'Sour', 7.0,True),
    Beer(5, 'Pilsner', 4.5,True),
    Beer(6, 'Lager', 4.5, True)
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
    friend_name = request.query_params.get('friend_name')
    if friend_name:
      friend_orders = [order for order in orders if order.friend_name == friend_name]
      total_value = sum(beer.price * order.quantity for order in friend_orders for beer in beers if order.beer_id == beer.id)
      return Response({'friend_name': friend_name, 'total_value': total_value})
    else:
      total_value = sum(beer.price * order.quantity for order in orders for beer in beers if order.beer_id == beer.id)
      return Response({'total_value': total_value})

class PayOrder(APIView):
  def post(self, request):
    payment_type = request.data.get('payment_type')
    if payment_type not in ['equal', 'individual']:
      return Response({'message': 'Invalid payment type'}, status=400)
    if payment_type == 'equal':
      if not orders:
        return Response({'message': 'No orders to pay'}, status=400)
      total_value = sum(beer.price * order.quantity for order in orders for beer in beers if order.beer_id == beer.id)
      if total_value == 0:
        return Response({'message': 'No orders found'}, status=400)
      value_friend = total_value / 3
      return Response({'message': f'Each friend should pay {value_friend:.2f}'})
    
    elif payment_type == 'individual':
      friend_name = request.data.get('friend_name')
      if not friend_name:
        return Response({'message': 'Friend name is required when individual payment type is choosed'}, status=400)
      individual_friend_orders = [order for order in orders if order.friend_name == friend_name]
      if not individual_friend_orders:
        return Response({'message': f'No orders found for {friend_name}'}, status=400)
      value_friend = sum(beer.price * order.quantity for order in individual_friend_orders for beer in beers if order.beer_id == beer.id)
      return Response({'message': f'{friend_name} should pay {value_friend:.2f}'})
    return Response({'message': 'Invalid request'}, status=400)

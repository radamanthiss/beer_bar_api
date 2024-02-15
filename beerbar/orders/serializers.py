from rest_framework import serializers

class BeerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    price = serializers.FloatField()
    is_available = serializers.BooleanField()

class OrderSerializer(serializers.Serializer):
    friend_name = serializers.CharField(max_length=100)
    beer_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
     
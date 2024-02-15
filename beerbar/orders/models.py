from django.db import models

# Create your models here.
class Beer:
  def __init__(self, id, name, price, is_available=True):
    self.id = id
    self.name = name
    self.price = price
    self.is_available = is_available

class Order:
  def __init__(self, friend_name, beer_id, quantity):
    self.friend_name = friend_name
    self.beer_id = beer_id
    self.quantity = quantity
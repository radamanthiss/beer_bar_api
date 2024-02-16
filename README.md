# beer_bar_api

API BEER
This project is a simple REST API built with Django and Django REST Framework (DRF) for managing beer orders it can be use for users to list available beers, create orders, and payments.

## Prerequisites
* Python
* pip
* virtualenv or conda management


## Installation
- clone the repo using this git clone https://github.com/radamanthiss/beer_bar_api.git
- virtualenv venv
- source venv/bin/activate or conda create -n beer_env python=3.9.18 if you have conda in your pc

## install requirements
- pip install -r requirements.txt

## start the project
- python manage.py migrate in this case is not necessary because we don't use database
- python manage.py runserver
- Your api is running at http://127.0.0.1:8000/

# API usage
## you can see the list of endpoints in the route http://127.0.0.1:8000/swagger/ or in next section each endpoint


## List beers endpoint
- endpoint GET /api/beers/
- desc : get all the list of available beers

## Receive an order endpoint
- endpoint POST /api/order/
- desc: create an order of beer
- paylodad
  {
  "beer_id": 1,
  "friend_name": "John Doe",
  "quantity": 2
  }


## Payment a order or account endpoint
- endpoint POST /api/pay/
- desc: using for payments can be equal or individual payment

### request for equal payment
- {"payment_type": 'equal'}

### request for individual payment
- {
    "payment_type":"individual",
    "friend_name":"Kevin"
  }

## Account endpoint
- endpoint GET /api/account/
- desc: get the values for account 

### request for all orders
- /api/account/
- response: {
    "total_value": 30.0
  }

### request for specific name from order
- /api/account/?friend_name=Kevin
- response: {
    "friend_name": "Kevin",
    "total_value": 25.0
  }

# RECOMENDATIONS
for a best performance to test the frontend, first call the endpoint for create and order to have data for test

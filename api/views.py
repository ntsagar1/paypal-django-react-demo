from django.shortcuts import render, redirect
import requests, json
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from settings.settings import PAYPAL_CLEINT_ID, PAYPAL_SECRET_ID


def index_page(request):
  return render(request, 'main.html', { 'PAYPAL_CLEINT_ID': PAYPAL_SECRET_ID })

## Get paypal access token
def get_paypal_access_token():
  get_token_url='https://api.sandbox.paypal.com/v1/oauth2/token'
  auth=(PAYPAL_SECRET_ID, PAYPAL_SECRET_ID)
  headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en_US',
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  payload = 'grant_type=client_credentials'
  result = requests.request("POST", get_token_url, headers=headers, auth=auth, data=payload)

  return result.json()

## Create order
def create_order():
  tokenResult = get_paypal_access_token()
  app_id = tokenResult.get('app_id')
  access_token = tokenResult.get('access_token')
  token_type = tokenResult.get('token_type')

  create_order_url = "https://api.sandbox.paypal.com/v2/checkout/orders"
  payload = {
    "intent": "CAPTURE",
    "purchase_units": [
      {
        "amount": {
          "currency_code": "USD",
          "value": "2.30"
        }
      }
    ]
  }
  payload = json.dumps(payload)
  headers = {
    'Content-Type': 'application/json',
    'Authorization': token_type + ' ' + access_token,
  }

  response = requests.request("POST", create_order_url, headers=headers, data=payload)
  return response.json()


## create order
def get_create_order(request):
  order = create_order()
  return JsonResponse(order, safe=False)

# ## test api
# def test_access_token(request):
#   result = get_paypal_access_token()
#   print(result.get('expires_in'))

  return JsonResponse(result, safe=False)

def charge_payment(order_id, paypal_request_id):

  tokenResult = get_paypal_access_token()
  access_token = tokenResult.get('access_token')
  token_type = tokenResult.get('token_type')

  payment_charge_url = "https://api.sandbox.paypal.com/v2/checkout/orders/"+ order_id +"/capture"
  payload = {}
  headers = {
    'Content-Type': 'application/json',
    'Authorization': token_type + ' ' + access_token,
    'PayPal-Request-Id': paypal_request_id
  }
  paymentRes = requests.request("POST", payment_charge_url, headers=headers, data = payload)

  return paymentRes.json()


def payment_charge_api(request, order_id, request_id):
  if not order_id:
    return JsonResponse({ 'error': 'Order id requred' }, safe=False)
  if not request_id:
    return JsonResponse({ 'error': 'request id requred' }, safe=False)

  if request.method == 'GET':
    return JsonResponse({ 'error': 'Only POST request allowed'}, safe=False)


  chargeResult = charge_payment(order_id, request_id)

  return JsonResponse(chargeResult, safe=False)

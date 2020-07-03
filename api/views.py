from django.shortcuts import render, redirect
import requests, json
from requests.auth import HTTPBasicAuth


from django.http import JsonResponse



CLEINT_ID=''
SECRET_ID=''



def index_page(request):
  return render(request, 'main.html', { 'PAYPAL_CLEINT_ID': CLEINT_ID })

## Get paypal access token
def get_paypal_access_token():
  get_token_url='https://api.sandbox.paypal.com/v1/oauth2/token'
  auth=(CLEINT_ID, SECRET_ID)
  headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en_US',
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  payload = 'grant_type=client_credentials'
  result = requests.request("POST", get_token_url, headers=headers, auth=auth, data=payload)

  return result.json()

def create_order():
  tokenResult = get_paypal_access_token()
  app_id = tokenResult.get('app_id')
  access_token = tokenResult.get('access_token')
  token_type = tokenResult.get('token_type')

  create_order_url = "https://api.sandbox.paypal.com/v2/checkout/orders"
  payment_data = {
    'price': 0.1,
    'description': 'table',
    'currency_code': 'USD'
  }
  payload = {
    "intent": "CAPTURE",
    "purchase_units": [
      {
        "amount": {
          "currency_code": "USD",
          "value": "0.2"
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

  # print(response.text.encode('utf8'))


## create order
def get_create_order(request):
  order = create_order()
  return JsonResponse(order, safe=False)

## test api
def send_json(request):
  result = get_paypal_access_token()
  print(result.get('expires_in'))

  return JsonResponse(result, safe=False)




def charge_payment(order_id):

  tokenResult = get_paypal_access_token()
  app_id = tokenResult.get('app_id')
  access_token = tokenResult.get('access_token')
  token_type = tokenResult.get('token_type')



  payment_charge_url = "https://api.sandbox.paypal.com/v2/checkout/orders/"+ app_id +"/capture"
  payload = {}
  headers = {
    'Content-Type': 'application/json',
    'Authorization': token_type + ' ' + access_token,
    'PayPal-Request-Id': order_id
  }
  paymentRes = requests.request("POST", url, headers=headers, data = payload)

  return paymentRes.json()


def payment_charge_api(request):
  order_id = request.POST.get('order_id', None)
  if not order_id:
    return JsonResponse({ 'error': 'Order id requred' }, safe=False)
  return JsonResponse({ 'error': 'Order id requred', 'order_id': order_id }, safe=False)

  # chargeResult = charge_payment(order_id)

  # return JsonResponse(chargeResult, safe=False)

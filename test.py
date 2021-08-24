import stripe
import pprint

from backend.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

# print("Customer")
# cus = stripe.Customer.create(
#     email='sid@gmail.com',
#     description = 'Sid Aximani'
# )

# print("Payment Intent")
# pay = stripe.PaymentIntent.create(
#     amount=87000,
#     currency='inr',
#     customer=cus['id']
# );print(pay)

print("Card")
card = stripe.PaymentMethod.create(
  type="card",
  card={
    "number": "4242424242424242",
    "exp_month": 8,
    "exp_year": 2022,
    "cvc": "314",
  },
)

print("Confirm")
# index = pay['client_secret'].index('_secret')
# id = pay['client_secret'][:index]
confirm = stripe.PaymentIntent.confirm(
    'pi_3JRiiDSCWQ7TprZS1BsKhQgg',
    payment_method=card['id']
)



# Client Secret = 'pi_3JRghMSCWQ7TprZS0ojxSBVh_secret_hBsyfcXHRVFhhRYaGzqOv7vuD
# PaymentIntent ID = 'pi_3JRghMSCWQ7TprZS0ojxSBVh
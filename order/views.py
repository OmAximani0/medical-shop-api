from order.serializer import NestedOrderSerializer, NestedOrderMedicineSerializer, OrderSerializer
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from rest_framework.response import Response
import json
from rest_framework import status
from order.models import Order, OrderMedicine
from medicine.models import Medicine, StoreMedicine
from store.models import Store
from users.models import Users
from uuid import uuid4
from datetime import datetime
from backend import settings
import stripe

from medicine.serializer import StoreMedicineSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


# add order
class AddOrderView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            user_id = requests.data["user_id"]
            store_id = requests.data["store_id"]
            medicines = requests.data["medicines"]
            address = requests.data['address']

            can_place_order = True
            total_amount = 0
            store = Store.objects.get(pk=store_id)
            for medicine_obj in medicines:
                medicine = Medicine.objects.get(pk=medicine_obj["medicine_id"])
                store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                if store_medicine.quantity >= medicine_obj["quantity"]:
                    total_amount += medicine_obj["quantity"] * store_medicine.price
                    continue
                can_place_order = False
                total_amount = 0
                break

            if can_place_order:

                user = Users.objects.get(pk=user_id)
                new_order = Order.objects.create(user_id=user, store_id=store, total_amount=total_amount, address=address)
                new_order.save()

                order = Order.objects.get(order_id=new_order.order_id)
                for medicine_obj in medicines:
                    medicine = Medicine.objects.get(pk=medicine_obj["medicine_id"])
                    store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                    new_quantity = store_medicine.quantity - medicine_obj["quantity"]

                    StoreMedicine.objects.filter(store_id=store, medicine_id=medicine).update(quantity=new_quantity)

                    new_order_medicine = OrderMedicine(order_id=order, medicine_id=medicine,
                                                       order_quantity=medicine_obj["quantity"])
                    new_order_medicine.save()

                total_amount = int(round(total_amount, 2) * 100)
                print(total_amount)
                customer = stripe.Customer.create(email=user.user_email)
                intent = stripe.PaymentIntent.create(
                    amount=total_amount,
                    currency='inr',
                    customer=customer['id']
                )
                response['clientSecret'] = intent['client_secret']
                response['order_id'] = order.order_id
                return Response(response, status=status.HTTP_200_OK)
            else:
                response['msg'] = "order failed"
        except Exception as e:
            print(e)
            response["error"] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# order success
class OrderSuccessView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            order_id = requests.get("order_id")
            Order.objects.filter(order_id=order_id).update(order_fulfilment_datetime=datetime.now(),
                                                           order_fulfilment_status="success")

            response = Response({
                "message": "payment done"
            })
        except Exception as e:
            print(e)
            response = Response(status=500)
        return response


# order cancel view
class OrderCancelView(GenericAPIView):
    def post(self, requests):
        try:
            response = {}
            secret_size = requests.data['clientSecret'].index('_secret')
            secert = requests.data['clientSecret'][:secret_size]

            order_id = requests.data["order_id"]
            order = Order.objects.get(pk=order_id)
            store = Store.objects.get(pk=order.store_id.store_id)
            order_medicines = OrderMedicine.objects.filter(order_id=order)
            for order_medicine in order_medicines:
                medicine = Medicine.objects.get(pk=order_medicine.medicine_id.medicine_id)
                refill_quantity = order_medicine.order_quantity
                store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                available_quantity = store_medicine.quantity
                new_quantity = available_quantity + refill_quantity
                StoreMedicine.objects.filter(store_id=store, medicine_id=medicine).update(quantity=new_quantity)
            Order.objects.filter(order_id=order_id).update(order_fulfilment_datetime=datetime.now(), order_fulfilment_status="cancelled")
            stripe.PaymentIntent.cancel(secert)
            response['msg'] = 'order cancelled successfully!'

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response['error'] = str(e)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# get order
class GetOrderView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            orders = requests.get("orders")
            data = []
            for order_id in orders:
                order = Order.objects.get(pk=order_id)
                order_medicine = OrderMedicine.objects.get(order_id=order)
                data.append({
                    "order_id": order.order_id,
                    "user_id": order.user_id,
                    "store_id": order.store_id,
                    "order_datetime": order.order_datetime,
                    "order_fulfilment_datetime": order.order_fulfilment_datetime,
                    "order_fulfilment_status": order.order_fulfilment_status,
                    "total_amount": order.total_amount,
                    "medicines": [
                        {
                            "medicine_id": medicine.medicine_id,
                            "quantity": medicine.quantity
                        } for medicine in order_medicine
                    ]
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)

class StoresAllOrderView(GenericAPIView):
    def post(self, request):
        try:
            response = []
            store_id = request.data['store_id']
            order_instance = Order.objects.filter(store_id=store_id, is_delivered=False)
            order_serializer = NestedOrderSerializer(order_instance, many=True)
            temp_dict = {}
            # Need to slice response
            for data in order_serializer.data:
                user = data['user_id']
                temp_dict['order_id'] = data['order_id']
                temp_dict['user_id'] = user['user_id']
                temp_dict['user_email'] = user['user_email']
                temp_dict['user_name'] = user['user_name']
                temp_dict['order_datetime'] = data['order_datetime']
                temp_dict['total_amount'] = data['total_amount']
                temp_dict['address'] = data['address']
                orderMedicine_instance = OrderMedicine.objects.filter(order_id = temp_dict['order_id'])
                orderMedicine_serializer = NestedOrderMedicineSerializer(orderMedicine_instance, many=True)
                for orderMedicine in orderMedicine_serializer.data:
                    medicine_obj = orderMedicine['medicine_id']
                    temp_dict['order_quantity'] = orderMedicine['order_quantity']
                    temp_dict['medicine_name'] = medicine_obj['medicine_name']
                response.append(temp_dict)
                temp_dict = {}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {'msg': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class OrderDeliveredView(GenericAPIView):
    def post(self, request):
        try:
            response = {}
            instance = Order.objects.get(order_id=request.data['order_id'])
            serializer = OrderSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['msg'] = "Deliverd!"
                return Response(response, status=status.HTTP_200_OK)
            response['error'] = serializer.error_messages
        except Exception as ex:
            print(ex)
            response['error'] = str(ex)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

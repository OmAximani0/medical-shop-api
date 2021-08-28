from django.urls import path

from order.views import AddOrderView, OrderSuccessView, OrderCancelView, GetOrderView, StoresAllOrderView, OrderDeliveredView

urlpatterns = [
    path('add/', AddOrderView.as_view()),
    path('success/', OrderSuccessView.as_view()),
    path('cancel/', OrderCancelView.as_view()),
    path('getorders/', GetOrderView.as_view()),

    path('bystore/', StoresAllOrderView.as_view()),
    path('delivered/', OrderDeliveredView.as_view()),
]

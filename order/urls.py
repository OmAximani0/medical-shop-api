from django.urls import path

from order.views import AddOrderView, OrderSuccessView, OrderCancelView, GetOrderView

urlpatterns = [
    path('addorders/', AddOrderView.as_view()),
    path('success/', OrderSuccessView.as_view()),
    path('cancel/', OrderCancelView.as_view()),
    path('getorders/', GetOrderView.as_view()),
]

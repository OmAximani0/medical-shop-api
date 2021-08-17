from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from . import views


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('logout/', views.LogOut.as_view(), name="logout_view"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('add/',views.AddUser.as_view(),name="add_user"),
    path('all/',views.GetAllUsers.as_view(),name="all_users"),
    path('update/', views.UpdateUser.as_view(), name="update_user"),
    path('delete/', views.DeleteUser.as_view(), name="delete_user"),
]
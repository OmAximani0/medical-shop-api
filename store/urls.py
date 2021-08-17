from django.urls import path

from store.views import AddStoreView, GetAllStoreView, GetStoreView, UpdateStoreView, DeleteStoreView, \
    StoresByMedicineView

urlpatterns = [
    path('addstores/', AddStoreView.as_view()),
    path('getallstores/', GetAllStoreView.as_view()),
    path('getstores/', GetStoreView.as_view()),
    path('updatestores/', UpdateStoreView.as_view()),
    path('deletestores/', DeleteStoreView.as_view()),

    path('getstoresbymedicine/', StoresByMedicineView.as_view()),
]

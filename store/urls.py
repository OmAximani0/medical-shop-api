from django.urls import path

from store.views import AddStoreView, GetAllStoreView, GetStoreView, UpdateStoreView, DeleteStoreView, \
    StoresByMedicineView

urlpatterns = [
    path('add/', AddStoreView.as_view()),
    path('all/', GetAllStoreView.as_view()),
    path('get/', GetStoreView.as_view()),
    path('update/', UpdateStoreView.as_view()),
    path('delete/', DeleteStoreView.as_view()),
    path('bymedicine/', StoresByMedicineView.as_view()),
    # path('search/medicine/<>')
]

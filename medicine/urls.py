from django.urls import path

from medicine.views import AddMedicineView, GetAllMedicineView, GetMedicineView, UpdateMedicineView, DeleteMedicineView, \
    AddStoreMedicineView, GetStoreMedicineView, UpdateStoreMedicineView, DeleteStoreMedicineView

urlpatterns = [
    path('addmedicines/', AddMedicineView.as_view()),
    path('getallmedicines/', GetAllMedicineView.as_view()),
    path('getmedicines/', GetMedicineView.as_view()),
    path('updatemedicines/', UpdateMedicineView.as_view()),
    path('deletemedicines/', DeleteMedicineView.as_view()),

    path('addstoremedicines/', AddStoreMedicineView.as_view()),
    path('getstoremedicines/', GetStoreMedicineView.as_view()),
    path('updatestoremedicines/', UpdateStoreMedicineView.as_view()),
    path('deletestoremedicines/', DeleteStoreMedicineView.as_view()),
]

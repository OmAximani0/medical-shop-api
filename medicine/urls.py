from django.urls import path

from medicine.views import AddMedicineView, GetAllMedicineView, GetMedicineView, UpdateMedicineView, DeleteMedicineView, \
    AddStoreMedicineView, GetStoreMedicineView, UpdateStoreMedicineView, DeleteStoreMedicineView

urlpatterns = [
    # Medicine
    path('add/', AddMedicineView.as_view()),
    path('all/', GetAllMedicineView.as_view()),
    path('get/', GetMedicineView.as_view()),
    path('update/', UpdateMedicineView.as_view()),
    path('delete/', DeleteMedicineView.as_view()),

    # Store Medicine
    path('addmedicine/', AddStoreMedicineView.as_view()),
    path('getmedicine/', GetStoreMedicineView.as_view()),
    path('updatemedicine/', UpdateStoreMedicineView.as_view()),
    path('deletemedicine/', DeleteStoreMedicineView.as_view()),
]

from django.urls import path
from .views import MeidicineList,MedicineDetails,MedicineDelete,MedicineUpdate,MedicineCreate
urlpatterns=[
    path('',MeidicineList.as_view(), name='home'),
    path('medicine/<int:pk>/', MedicineDetails.as_view(), name='details'),  
    path('medicine/create/', MedicineCreate.as_view(), name='create'),  
    path('medicine/update/<int:pk>/', MedicineUpdate.as_view(), name='update'),
    path('medicine/delete/<int:pk>/', MedicineDelete.as_view(), name='delete'),
]
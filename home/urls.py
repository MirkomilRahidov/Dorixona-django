from django.urls import path
from .views import MeidicineList,MedicineDetails,MedicineDelete,MedicineUpdate,MedicineCreate,MedicineApiList,MedecineApiCreate,MedicineApiDelete,MedicineApiUpdate
urlpatterns=[
    path('hone',MeidicineList.as_view(), name='home'),
    path('medicine/<int:pk>/', MedicineDetails.as_view(), name='details'),  
    path('medicine/create/', MedicineCreate.as_view(), name='create'),  
    path('medicine/update/<int:pk>/', MedicineUpdate.as_view(), name='update'),
    path('medicine/delete/<int:pk>/', MedicineDelete.as_view(), name='delete'),
    path('',MedicineApiList.as_view(), name='api'),
    path('api-create/',MedecineApiCreate.as_view(),name='create-api'),
    path("api-delete/<int:pk>/", MedicineApiDelete.as_view(), name="medicine-delete"),
    path("api-update/<int:pk>/", MedicineApiUpdate.as_view(), name="medicine-update"),
    
]   
from django.urls import path
from .views import MedicineDeleteAPIView,MedicineUpdateAPIView,MedicineListAPIView,MedicineCreateAPIView,UploadMedicineView #,MeidicineList ,MedicineDetails,MedicineDelete,MedicineUpdate,MedicineCreate,MedecineApiCreate,MedicineApiDelete,MedicineApiUpdate,MedicineListCreate,MedicineRetrieveDestroy
urlpatterns=[
    # path('hone',MeidicineList.as_view(), name='home'),
    # path('medicine/<int:pk>/', MedicineDetails.as_view(), name='details'),  
    # path('medicine/create/', MedicineCreate.as_view(), name='create'),  
    # path('medicine/update/<int:pk>/', MedicineUpdate.as_view(), name='update'),
    # path('medicine/delete/<int:pk>/', MedicineDelete.as_view(), name='delete'),
    # path('',MedicineApiList.as_view(), name='api'),
    # path('api-create/',MedecineApiCreate.as_view(),name='create-api'),
    # path("api-delete/<int:pk>/", MedicineApiDelete.as_view(), name="medicine-delete"),
    # path("api-update/<int:pk>/", MedicineApiUpdate.as_view(), name="medicine-update"),
    # path('api-list/', MedicineListCreate.as_view(), name='medicine-list'),
    # path('api-destroyupdate/<int:pk>/', MedicineRetrieveDestroy.as_view(), name='medicine-detail'),
    path('upload/', UploadMedicineView.as_view(), name='upload-medicine'),
    path("api-delete/<int:pk>/", MedicineDeleteAPIView.as_view(), name="medicine-delete"),
    path("api-update/<int:pk>/", MedicineUpdateAPIView.as_view(), name="medicine-update"),
    path('', MedicineListAPIView.as_view(), name='medicine-list'),
    path('api-create/', MedicineCreateAPIView.as_view(), name='medicine-create'),
    
    
]   
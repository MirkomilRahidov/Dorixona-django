from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse_lazy
from .models import Medicine
from .forms import MedicineForm
from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveDestroyAPIView,ListCreateAPIView
from .serializers import MedicineSerializer
from rest_framework.views import APIView
# class MeidicineList(View):
#     def get(self, request):
#         medicine = Medicine.objects.all()
#         return render(request, 'home.html', {'medicines': medicine})
# class MedicineDetails(View):
#     def get(self, request, pk):
#         medicine = Medicine.objects.get(pk=pk)
#         return render(request, 'details.html', {'medicine': medicine})
# class MedicineUpdate(View):
#     def get(self, request, pk):
#         medicine = get_object_or_404(Medicine, pk=pk)
#         form = MedicineForm(instance=medicine)
#         return render(request, 'update.html', {'form': form, 'medicine': medicine})

#     def post(self, request, pk):
#         medicine = get_object_or_404(Medicine, pk=pk)
#         form = MedicineForm(request.POST, request.FILES, instance=medicine)

#         if form.is_valid():
#             for field, value in form.cleaned_data.items():
#                 if value:  
#                     setattr(medicine, field, value)
#             medicine.save()
#             return redirect('details', pk=medicine.pk)

#         return render(request, 'update.html', {'form': form, 'medicine': medicine})
# class MedicineDelete(View):
#     def get(self, request, pk):
#         medicine = get_object_or_404(Medicine, pk=pk)
#         return render(request, 'delete.html', {'medicine': medicine})

#     def post(self, request, pk):
#         medicine = get_object_or_404(Medicine, pk=pk)
#         if 'confirm' in request.POST: 
#             medicine.delete()
#             return redirect('home')
#         return redirect('details', pk=medicine.pk)
# class MedicineCreate(View):
#     def get(self, request):
#         form = MedicineForm()
#         return render(request, 'create.html', {'form': form})

#     def post(self, request):
#         form = MedicineForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home') 
#         return render(request, 'create.html', {'form': form})
# class  MedicineApiList(ListAPIView):
#     queryset =Medicine.objects.all()
#     serializer_class = MedicineSerializer
# class MedecineApiCreate(CreateAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer 


# class MedicineApiDelete(DestroyAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     lookup_field = 'pk'


# class MedicineApiUpdate(UpdateAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     lookup_field = 'pk'


# class MedicineListCreate(ListCreateAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer


# class MedicineRetrieveDestroy(RetrieveDestroyAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#     lookup_field = 'pk'
class UploadMedicineView(View):
    def get(self, request):
        return render(request, "upload.html") 
class MedicineListAPIView(APIView):
    def get(self, request):
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True)
        rps = {"data": serializer.data, "status": status.HTTP_200_OK}
        return Response(rps)

class MedicineCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Dori muvaffaqiyatli qo‘shildi!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MedicineDeleteAPIView(APIView):
    def delete(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        medicine.delete()
        rps = {"message": "Medicine deleted successfully", "status": status.HTTP_204_NO_CONTENT}
        return Response(rps)

class MedicineUpdateAPIView(APIView):
    def put(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        serializer = MedicineSerializer(medicine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            rps = {"data": serializer.data, "status": status.HTTP_200_OK}
            return Response(rps)
        rps = {"data": serializer.errors, "status": status.HTTP_400_BAD_REQUEST}
        return Response(rps)

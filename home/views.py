from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from django.urls import reverse_lazy
from .models import Medicine
from .forms import MedicineForm
class MeidicineList(View):
    def get(self, request):
        medicine = Medicine.objects.all()
        return render(request, 'home.html', {'medicines': medicine})
class MedicineDetails(View):
    def get(self, request, pk):
        medicine = Medicine.objects.get(pk=pk)
        return render(request, 'details.html', {'medicine': medicine})
class MedicineUpdate(View):
    def get(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        form = MedicineForm(instance=medicine)
        return render(request, 'update.html', {'form': form, 'medicine': medicine})

    def post(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        form = MedicineForm(request.POST, request.FILES, instance=medicine)

        if form.is_valid():
            for field, value in form.cleaned_data.items():
                if value:  
                    setattr(medicine, field, value)
            medicine.save()
            return redirect('details', pk=medicine.pk)

        return render(request, 'update.html', {'form': form, 'medicine': medicine})
class MedicineDelete(View):
    def get(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        return render(request, 'delete.html', {'medicine': medicine})

    def post(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        if 'confirm' in request.POST: 
            medicine.delete()
            return redirect('home')
        return redirect('details', pk=medicine.pk)
class MedicineCreate(View):
    def get(self, request):
        form = MedicineForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request):
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Yangi dori qo‘shilgandan keyin asosiy sahifaga qaytadi
        return render(request, 'create.html', {'form': form})
    
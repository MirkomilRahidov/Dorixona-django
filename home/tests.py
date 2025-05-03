from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Medicine

class MedicineAPITestCase(APITestCase):
    def setUp(self):
        self.medicine = Medicine.objects.create(
            name="Paracetamol",
            description="Pain reliever and fever reducer",
            price=8.5
        )
        self.list_url = reverse('medicine-list') 
        self.create_url = reverse('medicine-create') 
        self.update_url = reverse('medicine-update', args=[self.medicine.pk])
        self.delete_url = reverse('medicine-delete', args=[self.medicine.pk])

    def test_list_medicines(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_create_medicine(self):
        data = {
            "name": "Ibuprofen",
            "description": "Anti-inflammatory drug",
            "price": 12.0
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 2)

    def test_update_medicine(self):
        data = {
            "price": 10.0
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh

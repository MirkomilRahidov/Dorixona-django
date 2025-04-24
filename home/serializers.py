from rest_framework import serializers
from .model import Medicine
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Medicine
        fields='__all__'
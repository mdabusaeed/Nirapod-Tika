from rest_framework import serializers
from .models import Vaccine, VaccinationSchedule

class VaccineSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField() 

    class Meta:
        model = Vaccine
        fields = '__all__'
        read_only_fields = ['created_by']  

class VaccinationScheduleSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()  

    class Meta:
        model = VaccinationSchedule
        fields = '__all__'
        read_only_fields = ['created_by']

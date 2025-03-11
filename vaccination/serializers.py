from rest_framework import serializers
from .models import Vaccine, VaccinationSchedule

class VaccineSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField() 

    class Meta:
        model = Vaccine
        fields = ['id', 'name', 'manufacturer', 'dose_intervals', 'doses_required','created_by']
        # read_only_fields = ['created_by']  



class VaccinationScheduleSerializer(serializers.ModelSerializer):
    vaccine_name = serializers.CharField(source='vaccine.name', read_only=True)
    dose_dates = serializers.ListField(child=serializers.DateField())  # Dose list Editable

    class Meta:
        model = VaccinationSchedule
        fields = ['id', 'patient', 'vaccine', 'vaccine_name', 'dose_dates']
        extra_kwargs = {'patient': {'read_only': True}}  # Patient নিজে সেট করতে পারবে না

    def update(self, instance, validated_data):
        """
        শুধুমাত্র Doctor dose_dates আপডেট করতে পারবে।
        """
        request = self.context['request']
        if request.user.role != 'doctor':  # শুধু Doctor update করতে পারবে
            raise serializers.ValidationError("Only doctors can modify the booking schedule.")

        instance.dose_dates = validated_data.get('dose_dates', instance.dose_dates)
        instance.save()
        return instance

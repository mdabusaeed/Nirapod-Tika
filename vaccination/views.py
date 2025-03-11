from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vaccine, VaccinationSchedule
from .serializers import VaccineSerializer, VaccinationScheduleSerializer

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer


    def perform_create(self, serializer):
        if self.request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can add vaccines.")
        serializer.save(created_by=self.request.user)  

class VaccinationScheduleViewSet(ModelViewSet):
    queryset = VaccinationSchedule.objects.all()
    serializer_class = VaccinationScheduleSerializer


    def perform_create(self, serializer):
        if self.request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can create vaccination schedules.")
        serializer.save(created_by=self.request.user)  


class PatientVaccinationHistoryViewSet(ModelViewSet):
    queryset = VaccinationSchedule.objects.all()
    serializer_class = VaccinationScheduleSerializer

    def get_queryset(self):
        return VaccinationSchedule.objects.filter(patient=self.request.user)
    
# class PatientVaccinationHistoryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         vaccinations = VaccinationSchedule.objects.filter(patient=request.user)
        
#         serializer = VaccinationScheduleSerializer(vaccinations, many=True)
        
#         return Response(serializer.data)
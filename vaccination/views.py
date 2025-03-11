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
    serializer_class = VaccinationScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Doctor সব রোগীর booking দেখতে পারবে,
        কিন্তু Patient শুধুমাত্র নিজের booking দেখতে পারবে।
        """
        user = self.request.user
        if user.role == 'doctor':
            return VaccinationSchedule.objects.all()  # Doctor সব booking দেখতে পারবে
        return VaccinationSchedule.objects.filter(patient=user)  # Patient শুধুমাত্র নিজেরটা দেখতে পারবে

    def update(self, request, *args, **kwargs):
        """
        শুধুমাত্র Doctor Vaccine Booking এর সময় পরিবর্তন করতে পারবে।
        """
        user = self.request.user
        if user.role != 'doctor':
            return Response({"error": "Only doctors can modify vaccine schedules."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)


class PatientVaccinationHistoryViewSet(ModelViewSet):
    queryset = VaccinationSchedule.objects.all()
    serializer_class = VaccinationScheduleSerializer

    def get_queryset(self):
        return VaccinationSchedule.objects.filter(patient=self.request.user)
    

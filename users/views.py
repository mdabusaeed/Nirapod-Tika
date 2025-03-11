from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView,CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from users.serializers import UserCreateSerializer 
from .models import User
from .serializers import UserSerializer
from vaccination.models import VaccinationSchedule  
from vaccination.serializers import VaccinationScheduleSerializer


    
class UserProfileView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        
        vaccinations = VaccinationSchedule.objects.filter(patient=request.user)
        vaccination_serializer = VaccinationScheduleSerializer(vaccinations, many=True)
        
        data = {
            "user_info": UserSerializer(user).data,
            "medical_details": user.medical_details,  
            "vaccination_history": vaccination_serializer.data
        }
        return Response(data)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        for field, value in serializer.validated_data.items():
            if value == "":
               
                continue
            setattr(user, field, value)
        
        user.save()  

        return Response(serializer.data)
    

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer



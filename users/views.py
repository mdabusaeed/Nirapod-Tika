from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView,CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from users.serializers import UserCreateSerializer 
from .models import User
from .serializers import UserSerializer,DoctorSerializer,ChangePasswordSerializer
from vaccination.models import VaccinationSchedule  
from vaccination.serializers import VaccinationScheduleSerializer


class UserProfileView(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        return self.request.user
    
    # def create(self, request, *args, **kwargs):
    #     return Response({"error": "User creation is not allowed. Use PUT or PATCH for updating your profile."}, status=400)
    
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
    

class DoctorProfileView(ModelViewSet):
    serializer_class = DoctorSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)  

    def get_object(self):
        return self.request.user 
    
    # def create(self, request, *args, **kwargs):
    #     return Response({"error": "User creation is not allowed. Use PUT or PATCH for updating your profile."}, status=400)

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class ChangePasswordViewSet(ModelViewSet):
    serializer_class = ChangePasswordSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)  

    def update(self, request, *args, **kwargs):
        """
        Update password for authenticated user.
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
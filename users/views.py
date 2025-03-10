from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView,CreateAPIView
from rest_framework.viewsets import ModelViewSet
from users.serializers import UserCreateSerializer 
from .models import User
from .serializers import UserSerializer

    
class UserProfileView(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer, UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('id', 'phone_number', 'password', 'first_name', 'last_name', 'address', 'email')
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUserSerializer"
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'address', 'email')
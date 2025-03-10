from django.urls import path, include
from rest_framework_nested import routers
from users.views import UserProfileView, UserRegistrationView


router = routers.DefaultRouter()
router.register('UserProfileView', UserProfileView)



urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),  
    path('auth/', include('djoser.urls.authtoken')),
    path('register/', UserRegistrationView.as_view(), name='user-register'),

]
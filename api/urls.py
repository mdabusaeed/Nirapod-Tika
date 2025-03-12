from django.urls import path, include
from rest_framework_nested import routers
from users.views import UserProfileView
from vaccination.views import VaccineViewSet, VaccinationScheduleViewSet, VaccineReviewViewSet, VaccineCampaignViewSet
from users.views import UserProfileView,DoctorProfileView,ChangePasswordViewSet


router = routers.DefaultRouter()
router.register('profile', UserProfileView, basename='profile')
router.register('vaccines', VaccineViewSet, basename = 'vaccine')
router.register('vaccination-schedules', VaccinationScheduleViewSet, basename = 'vaccination-schedules' )
router.register('doctor-profile', DoctorProfileView, basename='doctor-profile')
router.register('change-password', ChangePasswordViewSet, basename='change-password')
router.register('review', VaccineReviewViewSet, basename='review')
router.register('vaccine-campaign', VaccineCampaignViewSet, basename='vaccine-campaign')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),  
    path('auth/', include('djoser.urls.authtoken')),

]
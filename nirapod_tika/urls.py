from django.contrib import admin
from django.urls import path, include
import debug_toolbar  
# from .views import api_root_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', api_root_view),
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include(debug_toolbar.urls)),  
    path('api/v1/', include('api.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
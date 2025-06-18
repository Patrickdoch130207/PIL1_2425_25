from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trajets/', include('trajets.urls')),  
    path('chat/', include("chat.urls")),      
    path('', include('users.urls')),         
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Pour servir les fichiers statiques en mode développement

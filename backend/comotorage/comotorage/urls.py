# comotorage/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trajets/', include('trajets.urls')),  # Si vous avez cette app
    path('chat/', include("chat.urls")),      # Si vous avez cette app
    path('', include('users.urls')),          # URL racine (ajustez selon votre app principale)
]

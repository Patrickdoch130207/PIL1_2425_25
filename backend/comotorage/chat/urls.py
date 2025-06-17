from django.urls import path , include
from chat import views 
urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/users/', views.user_search, name='user_search'),  # Pour la recherche AJAX
    path('conversations/<str:email>/', views.conversation_detail, name='conversation_detail'),
]
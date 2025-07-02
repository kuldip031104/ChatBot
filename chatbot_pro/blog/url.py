from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chat-index'),
    path('getresponse/', views.get_response, name='get-response'),
]

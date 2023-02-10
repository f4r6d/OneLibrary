from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path('', views.MessageCreateView.as_view(), name="index"),
    path('messages/', views.get_messages, name='get-messages'),
]
from django.urls import path
from . import views

app_name = 'members'
urlpatterns = [
    path('register/', views.MyRegisterView.as_view(), name='register'),
]
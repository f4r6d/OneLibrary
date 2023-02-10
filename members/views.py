from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import MyUserCreationForm
from django.contrib.auth import login, authenticate


class MyRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = MyUserCreationForm
    template_name = 'members/register.html'
    success_url = reverse_lazy('catalog:index')
    success_message = 'Successfully Registered!'

    def get_success_url(self):
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(self.request, username=username, password=password)
        login(self.request,user)

        return super().get_success_url()



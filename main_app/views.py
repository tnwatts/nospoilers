from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# import the login_required decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Service, Group

# Add the following import
from django.http import HttpResponse

import urllib.request
import json
with urllib.request.urlopen("https://api.watchmode.com/v1/sources/?apiKey=o3vGEZAd7T47QHGt4xGr37yTiNP9HOJ8RCPGUDJu") as url:
    data = json.loads(url.read().decode())
    data = data[:10]



# Define the home view
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # add user to db
      user = form.save()
      Profile.objects.create(user_id=user.id, id=user.id)
      # automatically log in the new user
      login(request, user)
      # redirect to profile page with profile id -> redirect('profile', user_id=user_id)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message, 'data' : data}
  return render(request, 'registration/signup.html', context)

# def profile(request):
#     return render(request, 'profile.html')



class ProfileUpdate(UpdateView):
  model = Profile
  extra_context = {'serviceList': Service.objects.all(), }
  fields =  ['services']

  def get_available(self):
    profile_id = self.request.user.pk
    profile = Profile.objects.get(id=profile_id)
    id_list = profile.services.all().values_list('id')
    services_profile_doesnt_have = Service.objects.exclude(id__in=id_list)
    return services_profile_doesnt_have

def assoc_services(request, pk, service_id):
  profile = Profile.objects.get(id=pk)
  profile.services.add(service_id)
  return redirect('profile_update', pk=pk)

def unassoc_services(request, pk, service_id):
  profile = Profile.objects.get(id=pk)
  profile.services.remove(service_id)
  return redirect('profile_update', pk=pk)

class GroupCreate(CreateView):
  model = Group
  fields = '__all__'
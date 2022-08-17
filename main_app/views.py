from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Service, Group

import urllib.request
import json

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
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


# @login_required
def profile(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  serviceList=  Service.objects.all()
  services_ids = profile.services.all().values_list('id')
  services = Service.objects.exclude(id__in=services_ids)
  try:
    group = Group.objects.get(creator = profile)
    
  except:
    group = ''
  
  return render(request, 'profile.html',{'profile' : profile, 'serviceList' : serviceList, 'unowned_services' : services, 'group':group})

@login_required
def assoc_services(request, profile_id, service_id):
  profile = Profile.objects.get(id=profile_id)
  profile.services.add(service_id)
  return redirect('profile', profile_id=profile_id)

@login_required
def unassoc_services(request, profile_id, service_id):
  profile = Profile.objects.get(id=profile_id)
  profile.services.remove(service_id)
  return redirect('profile', profile_id=profile_id)


# @login_required
def create_group(request, profile_id):
  data = request.POST['pin']
  group_name = request.POST['name']
  group = Group.objects.create( name=group_name, creator_id=profile_id, pin=data)
  # retrieve services of creator for group's common services
  profile = Profile.objects.get(id=profile_id)
  services = profile.services.all()
  for service in services:
    group.services.add(service)
  print(group.services.all())
  # for service in group.services.all():
  #   print(service)
  return redirect('group_home', group_id=group.id)

@login_required
def group_home(request, group_id):
  group = Group.objects.get(id=group_id)
  api_id = group.services.all().values_list('api_id')
  with urllib.request.urlopen(f"https://api.watchmode.com/v1/list-titles/?apiKey=aSCkJNtfVnoaKWF2pphepbN97N7qdOtkvdxE4N4h&source_ids={api_id[0]}&sort_by=popularity_desc&types=tv_series") as url:
    data = json.loads(url.read().decode())
  show = data['titles'][0]
  with urllib.request.urlopen(f"https://api.watchmode.com/v1/title/{show['id']}/details/?apiKey=aSCkJNtfVnoaKWF2pphepbN97N7qdOtkvdxE4N4h") as url:
    data = json.loads(url.read().decode())
    print(data)
  show_details = data
  trailer_url = show_details['trailer'].replace('watch?v=', 'embed/')
  return render(request, 'group/home.html', {'group' : group, 'show' : show_details, 'trailer_url' : trailer_url})

@login_required
def assoc_accounts(request, profile_id):
  data = request.POST['pin']
  group_name = request.POST['name']
  group = Group.objects.get(pin=data, name=group_name)
  group.users.add(profile_id)
  # code below to determine group's common services

  # for each new user, loop through their services and check if its in the group's services already
  profile = Profile.objects.get(id=profile_id)
  # profile_services = profile.services.all()
  group_services = group.services.all()
  profile_services_ids = profile.services.all().values_list('id')
  services_not_in_profile = Service.objects.exclude(id__in=profile_services_ids)
  for service in services_not_in_profile:
    if service in group_services:
      group.services.remove(service)
 
  print(group.services.all())


  return redirect('group_home', group_id=group.id)


class GroupDelete(DeleteView, LoginRequiredMixin):
  model = Group
  success_url = '/'
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Service, Group


# Add the following import
from django.http import HttpResponse



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


def assoc_services(request, profile_id, service_id):
  profile = Profile.objects.get(id=profile_id)
  profile.services.add(service_id)
  return redirect('profile', profile_id=profile_id)


def unassoc_services(request, profile_id, service_id):
  profile = Profile.objects.get(id=profile_id)
  profile.services.remove(service_id)
  return redirect('profile', profile_id=profile_id)



def create_group(request, profile_id):
  data = request.POST['pin']
  group = Group.objects.create( name="Group", creator_id=profile_id, pin=data)
  return redirect('group_home', group_id=group.id)


def group_home(request, group_id):
  group = Group.objects.get(id=group_id)
 
  return render(request, 'group/home.html', {'group' : group})

def assoc_accounts(request, profile_id):
  data = request.POST['pin']
  group_name = request.POST['name']
  group = Group.objects.get(pin=data, name=group_name)
  group.users.add(profile_id)
  return redirect('group_home', group_id=group.id)


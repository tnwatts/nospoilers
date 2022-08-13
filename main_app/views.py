from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# import the login_required decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile

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
      Profile.objects.create(user_id=user.id)
    #   on signup method call{
    #     var = create profile 
    #     var.user_id = request.userid
    #   }
      # automatically log in the new user
      login(request, user)
      # redirect to profile page with profile id -> redirect('profile', user_id=user_id)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


# def profile(request):
#     return render(request, 'profile.html')

class ProfileUpdate(UpdateView):
  model = Profile
  fields = '__all__'


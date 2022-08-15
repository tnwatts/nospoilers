# from msilib.schema import ServiceInstall
from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# You can access the related information using Django's standard related model conventions:
# u = User.objects.get(username='fsmith')
# freds_department = u.employee.department

import urllib.request
import json
with urllib.request.urlopen("https://api.watchmode.com/v1/sources/?apiKey=o3vGEZAd7T47QHGt4xGr37yTiNP9HOJ8RCPGUDJu") as url:
    data = json.loads(url.read().decode())
    data = data[:10]

# Create your models here.


class Service(models.Model):
  name = models.CharField(max_length=50)
  api_id = models.CharField(max_length=6)
  logo = models.CharField(max_length=120)
  def __str__(self):
        return f"{self.name} {self.api_id} {self.logo}"
  def get_absolute_url(self):
      return reverse('service_detail', kwargs={'service_id': self.id})


# try:
#    obj = Service.objects.get(pk=1)
# except Service.DoesNotExist:
  

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  id = models.IntegerField(primary_key=True)
  services = models.ManyToManyField(Service)
  group = models.ForeignKey(
    on_delete=models.CASCADE
  )

  def __str__(self):
      return self.user.username

  def get_absolute_url(self):
      return reverse('profile_update', kwargs={'profile_id': self.id})

class Group(models.Model):
  creator = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(
    max_length=50,
  )

  def __str__(self):
        return f"Photo for rock_id: {self.rock_id} @{self.url}"

  def get_absolute_url(self):
    return reverse('groups_detail', kwargs={'group_id': self.id})

  

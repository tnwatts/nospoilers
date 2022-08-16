# from msilib.schema import ServiceInstall
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# You can access the related information using Django's standard related model conventions:
# u = User.objects.get(username='fsmith')
# freds_department = u.employee.department



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
  

  def __str__(self):
      return f"{self.user.username}"
  def get_absolute_url(self):
      return reverse('profile', kwargs={'profile_id': self.id})



class Group(models.Model):
  name = models.CharField(max_length=50)
  users = models.ManyToManyField(User)
  creator = models.OneToOneField(Profile, on_delete=models.CASCADE)
  pin = models.IntegerField(default=0000)
  def __str__(self):
    return f"{self.name}"
  def get_absolute_url(self):
    return reverse('group_home', kwargs={'group_id': self.id})
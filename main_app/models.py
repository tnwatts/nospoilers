# from msilib.schema import ServiceInstall
from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User

# You can access the related information using Django's standard related model conventions:
# u = User.objects.get(username='fsmith')
# freds_department = u.employee.department

# Create your models here.

SERVICES = [
  # replace with services model objects
  ('NF', 'Netflix'),
  ('HU', 'Hulu'),
  ('HM', 'HBO Max'),
  ('AP', 'Amazon Prime'),
]

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # favorite_color = models.CharField(max_length=50)
  services = models.CharField(
    max_length=len(SERVICES),
    choices=SERVICES,
    default=SERVICES[0][0]
  )
  # genres
  def __str__(self):
        return self.user.username

  def get_absolute_url(self):
    return reverse('profile_form', kwargs={'pk': self.id})

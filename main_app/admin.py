from django.contrib import admin
# import your models here
from .models import Profile, Service, Group
import os
import urllib.request
import json




service_names = []
service_ids = []
service_logos = []
  

@admin.action(description='Propogate Service Model')
def make_services(modeladmin, request, queryset):
    watchmode_api_key = os.environ['WATCHMODE_API_KEY']
    with urllib.request.urlopen(f"https://api.watchmode.com/v1/sources/?apiKey={watchmode_api_key}") as url:
        data = json.loads(url.read().decode())
    data = data[:20]
    for d in data:
        service_names.append(d['name'])
        service_ids.append(d['id'])
        service_logos.append(d['logo_100px'])
    for idx, s in enumerate(service_names):
        s = Service(name=s, api_id=service_ids[idx], logo=service_logos[idx])
        print(s)
        s.save()




# Register your models here
admin.site.register(Profile)
admin.site.register(Service)
admin.site.register(Group)
admin.site.add_action(make_services)

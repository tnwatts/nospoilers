from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('accounts/<int:pk>/assoc_services/<int:service_id>/', views.assoc_services, name='assoc_services'),
    path('accounts/<int:pk>/unassoc_services/<int:service_id>/', views.unassoc_services, name='unassoc_services'),
]
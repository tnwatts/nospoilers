from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/<int:profile_id>/', views.profile, name='profile'),
    path('accounts/<int:profile_id>/assoc_services/<int:service_id>/', views.assoc_services, name='assoc_services'),
    path('accounts/<int:profile_id>/unassoc_services/<int:service_id>/', views.unassoc_services, name='unassoc_services'),
    path('group/<int:group_id>/', views.group_home, name='group_home'),
    # path('accounts/<int:pk>/add_group/', views.add_group, name='add_group'),
    path('group/<int:profile_id>/create/', views.create_group, name='create_group'),
    # path('groups/<int:pk>/update/', views.GroupUpdate.as_view(), name='groups_update'),
    # path('groups/<int:pk>/delete/', views.GroupDelete.as_view(), name='groups_delete'),
]
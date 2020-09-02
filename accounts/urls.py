from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.user_profile_change, name='settings_profile'),
    path('deactivate/', views.DeactivateView.as_view(), name='settings_deactivate'),
    path('deactivate/done/', views.DeactivateDoneView.as_view(), name='settings_deactivate_done'),
]

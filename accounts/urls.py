from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.user_profile_change, name='settings_profile'),
    path('follow/<int:pk>/', views.accounts_follow_view, name='accounts_follow'),
    path('deactivate/', views.DeactivateView.as_view(), name='deactivate'),
    path('deactivate/done/', views.DeactivateDoneView.as_view(), name='deactivate_done'),
]

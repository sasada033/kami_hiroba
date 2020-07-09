from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.InquiryView.as_view(), name='inquiry'),
    path('thanks/', views.InquiryThanksView.as_view(), name='thanks'),
]
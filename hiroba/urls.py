
from django.urls import path

from . import views

app_name = 'hiroba'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('hiroba-list/', views.HirobaListView.as_view(), name="hiroba_list"),
    path('hiroba-detail/<int:pk>/', views.HirobaDetailView.as_view(), name="hiroba_detail"),
    path('hiroba-create/', views.HirobaCreateView.as_view(), name="hiroba_create"),
    path('hiroba-update/<int:pk>', views.HirobaUpdateView.as_view(), name="hiroba_update"),
    path('hiroba-delete/<int:pk>/', views.HirobaDeleteView.as_view(), name="hiroba_delete"),
    # path('hiroba-like/<int:pk>', views.HirobaLikeView.as_view(), name="hiroba-like"),
]
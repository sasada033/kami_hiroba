from django.urls import path
from . import views

app_name = 'khpost'

urlpatterns = [
    path('', views.KhpostIndexView.as_view(), name='index'),
    path('list/', views.KhpostListView.as_view(), name='khpost_list'),
    path('detail/<int:pk>/', views.KhpostDetailView.as_view(), name='khpost_detail'),
    path('create/', views.KhpostCreateView.as_view(), name='khpost_create'),
    path('update/<int:pk>/', views.KhpostUpdateView.as_view(), name='khpost_update'),
    path('delete/<int:pk>/', views.KhpostDeleteView.as_view(), name='khpost_delete'),
]
from django.urls import path
from . import views

app_name = 'khpost'

urlpatterns = [
    path('', views.KhpostIndexView.as_view(), name='index'),
    path('list/', views.KhpostListView.as_view(), name='khpost_list'),
    path('detail/<int:pk>/', views.khpost_detail, name='khpost_detail'),
    path('create/', views.khpost_create_view, name='khpost_create'),
    path('update/<int:pk>/', views.khpost_update_view, name='khpost_update'),
    path('delete/<int:pk>/', views.KhpostDeleteView.as_view(), name='khpost_delete'),
    path('like/<int:pk>/', views.khpost_like_view, name='khpost_like'),
]

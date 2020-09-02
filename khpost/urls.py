from django.urls import path
from . import views


app_name = 'khpost'

urlpatterns = [
    path('', views.KhpostIndexView.as_view(), name='index'),
    path('new/', views.KhpostListView.as_view(), name='khpost_list'),
    path('detail/<int:pk>/', views.KhpostDetailView.as_view(), name='khpost_detail'),
    path('create/', views.khpost_create_view, name='khpost_create'),
    path('update/<int:pk>/', views.khpost_update_view, name='khpost_update'),
    path('delete/<int:pk>/', views.KhpostDeleteView.as_view(), name='khpost_delete'),
    path('like/<int:pk>/', views.khpost_like_view, name='khpost_like'),
    path('follow/<int:pk>/', views.khpost_follow_view, name='khpost_follow'),
    path('<slug:slug>/', views.UserProfileIndexView.as_view(), name='khpost_profile'),
    path('<slug:slug>/deck/', views.UserProfileDeckView.as_view(), name='khpost_deck'),
    path('<slug:slug>/followers/', views.UserProfileFollowersView.as_view(), name='khpost_followers'),
]

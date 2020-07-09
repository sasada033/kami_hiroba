from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('search/', views.card_search_view, name='editor_search'),
]

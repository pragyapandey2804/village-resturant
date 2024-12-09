from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_comparison, name='restaurant_comparison'),  # Updated view function name
]

# restaurant_comparison/urls.py

from django.contrib import admin
from django.urls import path, include
from menu import views  # Import the views module from the menu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),  # Includes the menu app URLs
    path('', views.menu_comparison, name='home'),  # Add this line to handle the root URL
]

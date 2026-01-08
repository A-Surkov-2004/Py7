from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('polls/', include('polls.urls')),
    path('', include('accounts.urls')),
]
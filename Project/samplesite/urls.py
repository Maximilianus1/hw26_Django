from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('bboard/', include('bboard.urls', namespace='bboard')),
    path('admin/', admin.site.urls),
]


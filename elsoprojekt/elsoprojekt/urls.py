
from django.contrib import admin
from django.urls import path

from elsoapp.views import home_view, tesijel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proba/', home_view, name='home'),
    path('tesi/', tesijel),
]

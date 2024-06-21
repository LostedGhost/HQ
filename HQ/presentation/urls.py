from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('logout', logout, name='logout'),
]
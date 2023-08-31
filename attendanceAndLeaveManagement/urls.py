from django.urls import path
from .views import *

urlpatterns = [
    path("startTimer", startTimer),
    path("stopTimer", stopTimer),
]
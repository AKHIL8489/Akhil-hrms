from django.urls import path
from .views import *


urlpatterns = [
    path("recruitment/", jobPosting),
    path("viewAllJobs/",viewAllPostedJobs)
]
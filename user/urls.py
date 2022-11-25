

from django.urls import path
from .views import account, log_out, profile



urlpatterns = [
    path('',  account, name= "sign_in"),
    path('profile/',  profile, name= "profile"),
    path('log_out/',  log_out, name= "log_out"),
    # path('dashboard/',  dashboard, name= "dashboard"),
]
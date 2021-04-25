
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage,name="homepage"),
    path('about', views.aboutpage,name="aboutpage"),
    path('contact', views.contactpage,name="contactpage"),
    path('user', views.user_log_sign_page,name="userloginpage"),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('user/login', views.user_log_sign_page,name="userloginpage"),

]

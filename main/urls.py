
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage,name="homepage"),
    path('about', views.aboutpage,name="aboutpage"),
    path('contact', views.contactpage,name="contactpage"),
    path('user/', views.user_log_sign_page,name="userloginpage"),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('user/login', views.user_log_sign_page,name="userloginpage"),
    path('user/book-room', views.book_room_page,name="bookroom"),
    path('user/book-room/book', views.book_room,name="bookroom"),
    path('user/bookings', views.user_bookings,name="userbookings"),
    path('user/panel/change-status', views.user_change_status,name="userchangestatus"),
    path('logout', views.logoutuser,name="logout"),
    path('staff/', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/login', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignuppage"),
    path('staff/panel', views.panel,name="staffpanel"),
    path('staff/panel/add-new-hotel', views.add_new_hotel,name="addhotel"),
    path('staff/panel/add-new-room', views.add_new_room,name="addroom"),
    path('staff/panel/edit-room', views.edit_room,name="editroom"),
    path('staff/panel/edit-room/edit', views.edit_room,name="editroom"),
    path('staff/panel/view-room', views.view_room,name="viewroom"),
    path('staff/panel/change-status', views.change_status,name="changestatus"),

]

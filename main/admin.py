from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Hotel,Room,Reservation
from django.contrib.auth.models import User

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display=(('username', 'email', 'first_name', 'last_name', 'groups'))


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display=('name','owner','location','state','country')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=('ROOM_STATUS','room_type','capacity','price','size','hotel','status','roomnumber')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display=('check_in','check_out','room','guest','booking_id')




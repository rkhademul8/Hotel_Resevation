from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Hotel, Room, Reservation
# from django.contrib.admin.options import ModelAdmin



class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['pk', 'email', 'username', 'first_name', 'last_name']
    add_fieldsets = UserAdmin.add_fieldsets + (
    (None, {'fields': ('email', 'first_name', 'last_name', 'date_of_birth', 'address1', 'zip_code', 'city', 'country', 'mobile_phone', 'photo',)}),
)
    fieldsets = UserAdmin.fieldsets + (
    (None, {'fields': ( 'date_of_birth', 'address1',  'zip_code', 'city', 'country', 'mobile_phone', 'photo',)}),
)


admin.site.register(CustomUser, CustomUserAdmin)






# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#      list_display=('username', 'email', 'first_name', 'last_name', 'groups')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display=('name','owner','location','state','country')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=('ROOM_STATUS','room_type','capacity','price','size','hotel','status','roomnumber','Services')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display=('check_in','check_out','room','guest','booking_id')


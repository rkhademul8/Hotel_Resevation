from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Hotel(models.Model):
    #h_id,h_name,owner ,location,rooms
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 

    ROOM_TYPE = ( 
    ("1", "premium"), 
    ("2", "deluxe"),
    ("3","basic"),    
    ) 

    #type,no_of_rooms,capacity,prices,Hotel
    id = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=50,choices = ROOM_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    status = models.CharField(choices =ROOM_STATUS,max_length = 15)
    roomnumber = models.IntegerField()
    def __str__(self):
        return self.hotel.name

class Reservation(models.Model):

    id = models.AutoField(primary_key=True)
    check_in = models.DateField(auto_now =False)
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    guest = models.ForeignKey(User, on_delete= models.CASCADE)
    
    booking_id = models.CharField(max_length=100,default="null")
    def __str__(self):
        return self.guest.username

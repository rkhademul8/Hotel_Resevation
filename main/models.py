from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
# Create your models here.

class CustomUser(AbstractUser):
     date_of_birth = models.DateField(verbose_name=_("Date of birth"), blank=True, null=True)
     address1 = models.CharField(verbose_name=_("Address line 1"), max_length=1024, blank=True, null=True)
     zip_code = models.CharField(verbose_name=_("Postal Code"), max_length=12, blank=True, null=True)
     city = models.CharField(verbose_name=_("City"), max_length=1024, blank=True, null=True)
     country = CountryField(blank=True, null=True)
     phone_regex = RegexValidator(regex=r"^\+(?:[0-9]●?){6,14}[0-9]$", message=_("Enter a valid international mobile phone number starting with +(country code)"))
     mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_("Mobile phone"), max_length=17, blank=True, null=True)
     photo = models.ImageField(verbose_name=_("Photo"), upload_to='photos/', default='photos/default-user-avatar.png')

     class Meta:

         ordering = ['last_name']

     def __str__(self):
         return f"{self.username}: {self.first_name} {self.last_name}"




class Hotel(models.Model):
    #h_id,h_name,owner ,location,rooms
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=True)
    owner = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=50,null=True)
    photo=models.ImageField(upload_to='hotel/', null=True, blank=True)
    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_STATUS = ( 
    ("1", "available"), 
    ("2", "not available"),    
    ) 

    ROOM_TYPE = ( 
    ("1", "Premium"), 
    ("2", "Deluxe"),
    ("3","Economi"),    
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
    photo=models.ImageField(upload_to='room/', null=True, blank=True)
    Services=models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.hotel.name




class Reservation(models.Model):
    Reservation_STATUS = ( 
    ("1", "Pending"), 
    ("2", "Approved"),
    ("3", "Canceled"),      
    ) 
    
    status=models.CharField(choices=Reservation_STATUS, max_length=15, default="Pending")
    id = models.AutoField(primary_key=True)
    check_in = models.DateField(auto_now =False)
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    guest = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    payment_number=models.CharField(max_length=20, null=True, blank=True)
    trnxid=models.CharField(max_length=250,null=True, blank=True)
    booking_id = models.CharField(max_length=100,default="null")

    def __str__(self):
        return self.guest.username



    @property
    def total_price(self):
        days = (self.check_out - self.check_in).days
        result = self.room.price * days
        return result


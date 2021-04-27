from django.shortcuts import render ,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Hotel,Room,Reservation
import datetime


# Create your views here.

#homepage
def homepage(request):
    all_location = Hotel.objects.values_list('location','id').distinct().order_by()
    if request.method =="POST":
        try:
            print(request.POST)
            hotel = Hotel.objects.all().get(id=int(request.POST['search_location']))
            rr = []
            
            #for finding the reserved rooms on this time period for excluding from the query set
            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.room.id)
                
            room = Room.objects.all().filter(hotel=hotel,capacity__gte = int(request.POST['capacity'])).exclude(id__in=rr)
            if len(room) == 0:
                messages.warning(request,"Sorry No Rooms Are Available on this time period")
            data = {'rooms':room,'all_location':all_location,'flag':True}
            response = render(request,'index.html',data)
        except Exception as e:
            messages.error(request,e)
            response = render(request,'index.html',{'all_location':all_location})


    else:
        
        
        data = {'all_location':all_location}
        response = render(request,'index.html',data)
    return HttpResponse(response)


def aboutpage(request):
    return HttpResponse(render(request,'about.html'))

#contact page
def contactpage(request):
    return HttpResponse(render(request,'contact.html'))





#user sign up
def user_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request,"Password didn't matched")
            return redirect('userloginpage')
        
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Not Available")
                return redirect('userloginpage')
        except:
            pass
            

        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
        new_user.save()
        messages.success(request,"Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')




#user login and signup page
def user_log_sign_page(request):
    check = request.user
    if check.is_authenticated:
        return redirect('homepage')
    else:
            
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['pswd']

            user = authenticate(username=email,password=password)
            try:
                if user.is_staff:
                    
                    messages.error(request,"Incorrect username or Password")
                    return redirect('staffloginpage')
            except:
                pass
            
            if user is not None:
                login(request,user)
                messages.success(request,"successful logged in")
                return redirect('homepage')
            else:
                messages.warning(request,"Incorrect username or password")
                return redirect('userloginpage')

    response = render(request,'user/userlogsign.html')
    return HttpResponse(response)


#staff login and signup page
def staff_log_sign_page(request):
    check = request.user
    if check.is_authenticated:
        return redirect('homepage')
    else:

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username,password=password)
            
            if user.groups.filter(name='Hotel Owner').exists():
                login(request,user)
                messages.success(request,"successful logged in")
                return redirect('staffpanel')
            
            else:
                messages.success(request,"Incorrect username or password")
                return redirect('staffloginpage')
        response = render(request,'staff/stafflogsign.html')
        return HttpResponse(response)



#staff sign up
def staff_sign_up(request):
    if request.method =="POST":
        user_name = request.POST['username']
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request,"Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request,"Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass
        
        new_user = User.objects.create_user(username=user_name,password=password1)
        new_user.is_superuser=False
        new_user.is_staff=False
        new_user.save()
        group = Group.objects.get(name='Hotel Owner')
        new_user.groups.add(group)
        messages.success(request," Staff Registration Successfull")
        return redirect("staffloginpage")
    else:

        return HttpResponse('Access Denied')



#logout for admin and user 
def logoutuser(request):
    if request.method =='GET':
        logout(request)
        messages.success(request,"Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')


#staff panel page
@login_required(login_url='/staff')
def panel(request):
    if  request.user.groups.exists():
        user = request.user
        hotell = Hotel.objects.filter(owner=user)
        totall_rooms = []
        
        for hotels in hotell:
            room = Room.objects.filter(hotel=hotels)
            totall_rooms += room            
        total_rooms = len(totall_rooms)
        # available_rooms = len(Room.objects.all().filter(status='1'))
        # unavailable_rooms = len(Room.objects.all().filter(status='2'))
        # reserved = len(Reservation.objects.filter(room_hotel_owner=user))

        hotel = Hotel.objects.filter(owner=user)

        response = render(request,'staff/panel.html',{'name':hotel,'rooms':totall_rooms,'total_rooms':total_rooms})
        return HttpResponse(response)
    else:
        messages.success(request,"Access Denied")
        return redirect('homepage')



@login_required(login_url='/staff')
def add_new_hotel(request):
    if request.method == "POST":
        name = request.POST['hotel_name']
        user = request.user
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']
        
        # hotels = Hotel.objects.all().filter(location = location , state = state)
        # if hotels:
        #     messages.warning(request,"Sorry City at this Location already exist")
        #     return redirect("staffpanel")
        # else:
        new_hotel = Hotel()
        new_hotel.name = name
        new_hotel.owner = user
        new_hotel.location = location
        new_hotel.state = state
        new_hotel.country = country
        new_hotel.save()
        messages.success(request,"New Hotel Has been Added Successfully")
        return redirect("staffpanel")

    else:
        messages.warning(request,"Not Allowed")
        return redirect('homepage')



@login_required(login_url='/staff')
def add_new_room(request):
    if request.method == "POST":
        total_rooms = len(Room.objects.all())
        new_room = Room()
        hotel = Hotel.objects.all().get(id = int(request.POST['hotel']))
        new_room.roomnumber = total_rooms + 1
        new_room.room_type  = request.POST['roomtype']
        new_room.capacity   = int(request.POST['capacity'])
        new_room.size       = int(request.POST['size'])
        new_room.capacity   = int(request.POST['capacity'])
        new_room.hotel      = hotel
        new_room.status     = request.POST['status']
        new_room.price      = request.POST['price']

        new_room.save()
        messages.success(request,"New Room Added Successfully")
    
    return redirect('staffpanel')



#for editing room information
@login_required(login_url='/staff')
def edit_room(request):
    if request.method == 'POST':
        old_room = Room.objects.all().get(id= int(request.POST['roomid']))
        hotel = Hotel.objects.all().get(id=int(request.POST['hotel']))
        old_room.room_type  = request.POST['roomtype']
        old_room.capacity   =int(request.POST['capacity'])
        old_room.price      = int(request.POST['price'])
        old_room.size       = int(request.POST['size'])
        old_room.hotel      = hotel
        old_room.status     = request.POST['status']
        old_room.room_number=int(request.POST['roomnumber'])

        old_room.save()
        messages.success(request,"Room Details Updated Successfully")
        return redirect('staffpanel')
    else:
    
        room_id = request.GET['roomid']
        room = Room.objects.all().get(id=room_id)
        response = render(request,'staff/editroom.html',{'room':room})
        return HttpResponse(response)




# view room information
@login_required(login_url='/staff')   
def view_room(request):
    room_id = request.GET['roomid']
    room = Room.objects.all().get(id=room_id)

    reservation = Reservation.objects.all().filter(room=room)
    return HttpResponse(render(request,'staff/viewroom.html',{'room':room,'reservations':reservation}))


# booked dashboard
@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        messages.error(request,"Please login to Book rooms")
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    bookings = Reservation.objects.all().filter(guest=user)
    total = 0
    for book in bookings:
        checkin = book.check_in
        checkout = book.check_out
        price = book.room.price
        total += price * (checkout - checkin).days

    if not bookings:
        messages.warning(request,"No Bookings Found")
    return HttpResponse(render(request,'user/mybookings.html',{'bookings':bookings, 'total':total}))



#For booking the room
@login_required(login_url='/user')
def book_room(request):
    if request.method =="POST":
        room_id = request.POST['room_id']
        room = Room.objects.all().get(id=room_id)
        #for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(room = room):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request,"Sorry This Room is unavailable for Booking")
                return redirect("homepage")
            
        current_user = request.user
        total_person = int( request.POST['person'])
        booking_id = str(room_id) + str(datetime.datetime.now())

        reservation = Reservation()
        room_object = Room.objects.all().get(id=room_id)
        room_object.status = '2'
        
        user_object = User.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.room = room_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request,"Congratulations! Booking Successfull")

        return redirect("userbookings")
    else:
        return HttpResponse('Access Denied')


#booking room page
@login_required(login_url='/user')
def book_room_page(request):
    room = Room.objects.all().get(id=int(request.GET['roomid']))
    return HttpResponse(render(request,'user/bookroom.html',{'room':room}))


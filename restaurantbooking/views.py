from django.shortcuts import render, redirect

# Create your views here.

from datetime import datetime, timedelta
from .models import *
from django.contrib import messages

def index(request):
    return render(request, "index.html",{})

def booking(request):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(28)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('groupsize')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "Please Select The Group Size!")
            return redirect('booking')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['groupsize'] = groupsize

        return redirect('bookingSubmit')

    return render(request, 'booking.html', {
            'weekdays' : weekdays,
            'validateWeekdays' : validateWeekdays,
        })

def bookingSubmit(request):
    user = request.user
    times = [
        "12 PM", "12:30 PM", "1 PM", "1:30 PM", "3 PM", "3:30 PM", "4 PM", "4:30 PM",
        "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM","8 PM", "8:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if groupsize != None:
            if day <= maxDate and day >= minDate:
                if date == 'Tuesday' or date == 'Wednesday'or date == 'Thursday' or date == 'Friday'or date == 'Saturday':
                    if Reservation.objects.filter(day=day).count() < 19:
                        if Reservation.objects.filter(day=day, time=time).count() < 1:
                            ReservationForm = Reservation.objects.get_or_create(
                                user = user,
                                groupsize = groupsize,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Reservation Saved!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "No availability on the selected day!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select The Group Size!")


    return render(request, 'bookingSubmit.html', {
        'times':hour,
    })

def userPanel(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).order_by('day', 'time')
    return render(request, 'userPanel.html', {
        'user':user,
        'reservations':reservations,
    })

def userUpdate(request, id):
    reservation = Reservation.objects.get(pk=id)
    userdatepicked = reservation.day
    #Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    #24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        groupsize = request.POST.get('groupsize)
        day = request.POST.get('day')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['groupsize'] = groupsize

        return redirect('userUpdateSubmit', id=id)


    return render(request, 'userUpdate.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
            'delta24': delta24,
            'id': id,
        })

def userUpdateSubmit(request, id):
    user = request.user
    times = [
        "12 PM", "12:30 PM", "1 PM", "1:30 PM", "3 PM", "3:30 PM", "4 PM", "4:30 PM",
        "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM","8 PM", "8:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    groupsize = request.session.get('groupsize')
    
    #Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    reservation = Reservation.objects.get(pk=id)
    userSelectedTime = reservation.time
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if groupsize != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Reservation.objects.filter(day=day).count() < 11:
                        if Reservation.objects.filter(day=day, time=time).count() < 1 or userSelectedTime == time:
                            ReservationForm = Reservation.objects.filter(pk=id).update(
                                user = user,
                                groupsize = groupsize,
                                day = day,
                                time = time,
                            ) 
                            messages.success(request, "Reservation Changed!")
                            return redirect('index')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "There is no availability on the selected day!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select The Group Size!")
        return redirect('userPanel')


    return render(request, 'userUpdateSubmit.html', {
        'times':hour,
        'id': id,
    })

def staffPanel(request):
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime
    #Only show the Appointments 21 days from today
    items = Reservation.objects.filter(day__range=[minDate, maxDate]).order_by('day', 'time')

    return render(request, 'staffPanel.html', {
        'items':items,
    })

def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Reservation.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Reservation.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    reservation = Reservation.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x

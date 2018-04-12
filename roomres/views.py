from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from roomres.models import Room, Reservation


def add_room(request):
    if request.method == 'GET':
        return render(request, 'new.html', {})
    else:
        if request.POST['action'] == 'Add':
            name = request.POST.get('name')
            capacity = request.POST.get('capacity')
            projector = request.POST.get('projector')
            response = HttpResponse()
            if (name, capacity, projector) is not None:
                Room.objects.create(name=name, capacity=int(capacity), projector=projector)
                response.write('Room has been added')
            else:
                response.write('Provide correct data')
            return response
        else:
            return redirect('/')


def modify_room(request, my_id):
        room = get_object_or_404(Room, id=int(my_id))
        if request.method == 'GET':
            return render(request, 'modify.html', {'room': room})
        else:
            if request.POST['action'] == 'Change':
                name = request.POST.get('name')
                capacity = request.POST.get('capacity')
                projector = request.POST.get('projector')
                room.projector = projector
                if name:
                    room.name = name
                if capacity:
                    room.capacity = int(capacity)
                room.save()
                return HttpResponse('Dane zostały zmienione')
            else:
                return redirect('/')


def delete_room(request, my_id):
    room = get_object_or_404(Room, id=int(my_id))
    room.delete()
    return HttpResponse('Room has been deleted')


def show_room(request, my_id):
    room = get_object_or_404(Room, id=int(my_id))
    today = date.today()
    dates = room.reservation_set.all()
    dates = dates.filter(date__gte=today)
    return render(request, 'show.html', {'room': room, 'dates': dates})


def show_rooms(request):
    today = date.today()
    name = request.GET.get('name')
    user_date = request.GET.get('date')
    capacity = request.GET.get('capacity')
    projector = request.GET.get('projector')
    rooms = Room.objects.all()
    if name:
        rooms = rooms.filter(name__icontains=name)
    if capacity:
        rooms = rooms.filter(capacity__gte=int(capacity))
    if projector == 'available':
        rooms = rooms.filter(projector=True)
    if projector == 'not available':
        rooms = rooms.filter(projector=False)
    if user_date:
        today = user_date
    available_list = []
    for room in rooms:
        if room.reservation_set.filter(date=today):
            available_list.append(room)
            today = str(today)
    return render(request, 'show_all.html', {'rooms': rooms, 'list': available_list, 'name': name,
                                             'today': today, 'capacity': capacity, 'projector': projector})


def reservation(request, my_id):
    if request.POST['action'] == 'Book':
        today = date.today()
        user_date = request.POST.get('date')
        comment = request.POST.get('comment')
        room = Room.objects.get(id=int(my_id))
        book = Reservation.objects.filter(room=room)
        if user_date:
            user_date = datetime.strptime(user_date, '%Y-%m-%d').date()
        else:
            return HttpResponse('You added wrong data')
        if book:
            book_list = []
            for row in book:
                book_list.append(row.date)
            if user_date in book_list or user_date < today:
                return HttpResponse('You added wrong data')
            Reservation.objects.create(date=str(user_date), room=room, comment=comment)
            return redirect('/')
    else:
        return redirect('/')

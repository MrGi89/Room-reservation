from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from roomres.models import Room, Reservation


class WelcomeView(View):

    def get(self, request):

        return render(request, template_name='roomres/show_rooms.html', context={})


class ShowRoomsView(View):

    def get(self, request):

        rooms = Room.objects.all()
        return render(request, template_name='roomres/show_rooms.html', context={'rooms': rooms})


class ShowRoomView(View):

    def get(self, request, room_pk):

        room = Room.objects.get(pk=room_pk)
        return render(request, template_name='roomres/show_room.html',  context={'room': room})


# def show_rooms(request):
#     today = date.today()
#     name = request.GET.get('name')
#     user_date = request.GET.get('date')
#     capacity = request.GET.get('capacity')
#     projector = request.GET.get('projector')
#     rooms = Room.objects.all()
#     if name:
#         rooms = rooms.filter(name__icontains=name)
#     if capacity:
#         rooms = rooms.filter(capacity__gte=int(capacity))
#     if projector == 'available':
#         rooms = rooms.filter(projector=True)
#     if projector == 'not available':
#         rooms = rooms.filter(projector=False)
#     if user_date:
#         today = user_date
#     available_list = []
#     for room in rooms:
#         if room.reservation_set.filter(date=today):
#             available_list.append(room)
#             today = str(today)
#     return render(request, 'show_all.html', {'rooms': rooms, 'list': available_list, 'name': name,
#                                              'today': today, 'capacity': capacity, 'projector': projector})


class NewRoomView(CreateView):

    model = Room
    fields = '__all__'
    template_name = 'roomres/new_room.html'

    def form_valid(self, form):
        instance = form.save()
        return redirect(self.get_success_url(room_id=instance.id))

    def get_success_url(self, **kwargs):

        room_id = kwargs['room_id']
        return reverse_lazy('show', kwargs={'room_id': room_id})




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


def show_room(request, room_id):
    room = get_object_or_404(Room, id=int(room_id))
    today = date.today()
    dates = room.reservation_set.all()
    dates = dates.filter(date__gte=today)
    return render(request, 'show.html', {'room': room, 'dates': dates})




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

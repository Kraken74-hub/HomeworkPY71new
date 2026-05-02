from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Table, Reservation
from .forms import ReservationForm
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def table_list(request):
    seats_filter = request.GET.get('seats')
    tables = Table.objects.all()
    if seats_filter:
        tables = tables.filter(seats__gte=seats_filter)
    return render(request, 'bookings/tables_list.html', {'tables': tables})

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        form.user = request.user # Для валидации количества броней
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('my_reservations')
    else:
        initial_table = request.GET.get('table_id')
        form = ReservationForm(initial={'table': initial_table})
    return render(request, 'bookings/reservation_form.html', {'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bookings/my_reservations.html', {'reservations': reservations})
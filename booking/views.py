from django.shortcuts import render, redirect
from .models import Doctor, Appointment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# 🏠 HOME
def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'booking/home.html', {'doctors': doctors})


# 👨‍⚕️ DOCTORS
def doctors(request):
    search = request.GET.get('search')
    specialization = request.GET.get('specialization')

    doctors = Doctor.objects.all()

    if search:
        doctors = doctors.filter(name__icontains=search)

    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    return render(request, 'booking/doctors.html', {'data': doctors})


# 📅 BOOK
def book(request):
    doctors = Doctor.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        doctor = Doctor.objects.get(id=doctor_id)

        # Prevent duplicate booking
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            return render(request, 'booking/booking.html', {
                'doctors': doctors,
                'error': 'Slot already booked!'
            })

        Appointment.objects.create(
            patient_name=name,
            phone=phone,
            email=email,
            doctor=doctor,
            date=date,
            time=time
        )

        return redirect('/appointments/')

    return render(request, 'booking/booking.html', {'doctors': doctors})


@login_required
def appointments(request):
    data = Appointment.objects.all()
    return render(request, 'booking/appointments.html', {'data': data})


# 🔐 ADMIN LOGIN
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin-dashboard/')
        else:
            return render(request, 'booking/admin_login.html', {'error': 'Invalid Credentials'})

    return render(request, 'booking/admin_login.html')


# 📊 ADMIN DASHBOARD (FIXED)
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/admin-login/')

    data = Appointment.objects.all()
    return render(request, 'booking/admin_dashboard.html', {'data': data})


# 🚪 LOGOUT
def admin_logout(request):
    logout(request)
    return redirect('/admin-login/')


# ❌ DELETE (FIXED)
def delete_appointment(request, id):
    appt = get_object_or_404(Appointment, id=id)
    appt.delete()
    return redirect('/appointments/')


# 🔄 UPDATE STATUS (FIXED)
def update_status(request, id, status):
    appt = get_object_or_404(Appointment, id=id)
    appt.status = status
    appt.save()
    return redirect('/appointments/')

from django.shortcuts import get_object_or_404

def approve_appointment(request, id):
    obj = get_object_or_404(Appointment, id=id)
    obj.status = "Approved"
    obj.save()
    return redirect('appointments')


def reject_appointment(request, id):
    obj = get_object_or_404(Appointment, id=id)
    obj.status = "Rejected"
    obj.save()
    return redirect('appointments')


def delete_appointment(request, id):
    obj = get_object_or_404(Appointment, id=id)
    obj.delete()
    return redirect('appointments')
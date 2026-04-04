from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    available_days = models.CharField(max_length=100)
    available_time = models.CharField(max_length=100)

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    patient_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='Booked')
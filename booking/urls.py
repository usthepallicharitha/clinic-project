from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctors, name='doctors'),
    path('book/', views.book, name='book'),
    path('appointments/', views.appointments, name='appointments'),

    # Admin
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Actions
    path('approve/<int:id>/', views.approve_appointment, name='approve'),
    path('reject/<int:id>/', views.reject_appointment, name='reject'),
    path('delete/<int:id>/', views.delete_appointment, name='delete'),
]
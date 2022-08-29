from django.contrib import admin
from django.urls import path, include

from testApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dr/', views.doctor, name='doctorPage'),
    path('patient/', views.patient, name='patientPage'),
    path('Login/', views.Login, name='login'),
    path('Register/', views.Register, name='register'),
    path('Logout/', views.Logout_, name='logout'),
    path('Appointments/', views.appoint, name='appointList'),
    path('accept/<int:ap_id>/', views.acceptAppointment, name='acceptAppointment'),
    path('delete/<int:ap_id>', views.deleteAppointment, name='deleteAppointment'),

]

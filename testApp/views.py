from datetime import date, datetime
from django.core.mail import send_mail
from .models import Appointments, UserProfile, MyUser
from django.shortcuts import redirect, render, HttpResponse
from .forms import RegisterationForm, LoginForm, DateTimeField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import pytz
utc = pytz.UTC
max_consulting_time = 30

# Create your views here.


@login_required(login_url='login')
def acceptAppointment(request, ap_id):
    appointment = Appointments.objects.get(id=ap_id)
    send_mail(
        subject='Appointment Booked',
        message=f'''Description : {appointment.desc}\n\nAppointment Date & Time : {appointment.date_time.date()} {appointment.date_time.time()}''',
        from_email='rajsingh08471@gmail.com',
        recipient_list=[appointment.emailField],
    )
    appointment.delete()
    request.session['count'] -= 1
    if request.user.userprofile == 'Patient':
        return redirect('appointList')
    else:
        return redirect('doctorPage')


@login_required(login_url='login')
def deleteAppointment(request, ap_id):
    appointment = Appointments.objects.get(id=ap_id).delete()
    request.session['count'] -= 1
    if request.user.userprofile.role == 'Patient':
        return redirect('appointList')
    else:
        return redirect('doctorPage')


@login_required(login_url='login')
def index(request):
    if(request.user.userprofile.role == "Patient"):
        appointments_count = Appointments.objects.filter(
            patient_name=request.user.username).count()
        # request.user.count = appointments_count
        request.session['count'] = appointments_count
    else:
        appointments_count = request.user.appointments_set.count()
        request.session['count'] = appointments_count
        print(request.session['count'])

    return render(request, 'index.html', {'appointments_cnt': appointments_count})


@ login_required(login_url='login')
def doctor(request):
    appointMentList = request.user.appointments_set.all()
    print(appointMentList)
    return render(request, 'appointmentsMade.html', {'Appointments': appointMentList, 'User': request.user.userprofile.role})


@ login_required(login_url='login')
def appoint(request):

    appointMentList = Appointments.objects.filter(
        patient_name=request.user.username)
    return render(request, 'appointmentsMade.html', {'Appointments': appointMentList, 'User': request.user.userprofile.role})


@ login_required(login_url='login')
def patient(request):
    if request.method == 'POST':
        date_time = DateTimeField(request.POST)
        if date_time.is_valid():
            dt = date_time.cleaned_data['date_time']
            if(not handleSlotSchedules(dt)):
                messages.error(request, 'This slot is already booked')
                return redirect('patientPage')
            else:
                email = request.POST['email']
                desc = request.POST['desc']
                phoneNum = request.POST['phoneNum']
                doctorEmail = request.POST['doctor_name']
                doctor = MyUser.objects.get(email=doctorEmail)
                appointMent = Appointments.objects.create(
                    user=doctor, desc=desc, emailField=email, contact=phoneNum, date_time=dt, patient_name=request.user.username)
                request.session['count'] += 1
                return redirect('appointList')
            

    doctorList = UserProfile.objects.filter(role='Doctor')
    dateTime = DateTimeField()
    context = {'doctors_list': doctorList, "form": dateTime}
    return render(request, 'patient.html', context)


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.errors)
        str_ = form.non_field_errors()
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password_']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                print("User Found")
                login(request, user)
                print(user.userprofile.role)
                if user.userprofile.role == 'Patient':
                    return redirect('patientPage')
                else:
                    return redirect('doctorPage')
            else:
                print("User Not Found")
                return redirect('register')
        else:
            return HttpResponse(str_)
    else:
        form = LoginForm()
        return render(request, 'Login.html', {'form': form})


def Register(request):
    if request.method == 'POST':
        role = request.POST['selectInputData']
        form = RegisterationForm(request.POST)
        print("********", form.errors, "************")
        if form.is_valid():
            user = form.save()
            userProfile = UserProfile.objects.create(user=user, role=role)
            print(user)
            print("*****")
            print(userProfile)
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterationForm()
        print("fail")
        return render(request, 'register.html', {'form': form})


def Logout_(request):
    logout(request)
    return redirect('login')


def handleSlotSchedules(dateTime):
    dateTime = dateTime.replace(tzinfo=utc)
    now = datetime.now()
    now = now.replace(tzinfo=utc)
    appointments = Appointments.objects.filter(date_time__date=dateTime.date())
    for appointment in appointments:
        print(appointment.date_time.date())
        tmp = dateTime - appointment.date_time
        tmp = tmp.total_seconds()/60
        print("tmp", tmp)
        if(tmp < max_consulting_time):
            return False

    return True

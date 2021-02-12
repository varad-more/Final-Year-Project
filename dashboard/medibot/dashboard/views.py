from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime,timedelta

from contextlib import contextmanager
#Twilio - SMS Module
from twilio.rest import Client
from django.conf import settings  

from dashboard.models import *
# from dashboard.models import patient

#Report Uploader Module
from modules import report_extraction_final
import json
# from werkzeug.utils import secure_filename
from django.core.files.storage import FileSystemStorage 
import os
from .forms import *


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
allowed_file = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4' ,''])


""" 
The decorator for checking if user or admin is signed in.
If user is not logged in is redirected to signin

"""

def doctor_logged_in(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_role' not in request.session.keys():
                    request.session['error'] = "You are not authorized to view the page. Sign In to view."
                    return redirect("signin")
                
                elif request.session['user_role'] == 'doctor' :
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap

def receptionist_logged_in(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_role' not in request.session.keys():
                    request.session['error'] = "You are not authorized to view the page. Sign In as Receptionist to view."
                    return redirect("signin")
                
                elif request.session['user_role'] == 'receptionist' :
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


def admin_logged_in(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_role' not in request.session.keys():
                    return redirect("signin")
                
                elif request.session['user_role'] == 'admin' :
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


def hash_password (password):
    import hashlib
    import os

    # salt = os.urandom(32) # Remember this
    salt = b'varad'
    # key = b'\x07\x0fV=<\xe7r\xa7\x85\xe5\xe44H>\\\x13\xad\x18l\xba~\xe4\xb1\x99\x96cz\xb4\x92\x94\x829'
    # print ('salt', salt)
    # password = 'password123'

    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )

    return key


def sign_in(request):
    print ('signin')

    if request.method == 'POST' :
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        entered_key = hash_password(password)
        login_user = user.objects.filter(email=email, password=password).first()

        # To be hashed
        login_user1 = user.objects.filter(email=email, password=entered_key).first()

        print (login_user)

        if login_user or login_user1:
            request.session['user_role'] = login_user.user_role
            request.session['email'] = login_user.email
            request.session['id'] = login_user.id

            return redirect ('patient_information')
        
        else:

            print('Bad Credentials')
            content = {'error': 'Password Incorrect'}
            return render (request, 'sign_in.html', content)

    # if 'error'  in request.session.keys():
    #     content = { 'error': request.session['error']}
    #     del request.session['error']
    content={}
    return render (request, 'sign_in.html', content)


def sign_up(request):

    print ('sign up')
    if request.method == 'POST' :
        
        passd = request.POST.get('pass')
        
        new_user = user()
        new_user.name = request.POST.get('name')
        new_user.email = request.POST.get('email')
        new_user.age = request.POST.get('age')
        new_user.gender = request.POST.get('gender')
        new_user.phone = request.POST.get('phone')
        new_user.password = hash_password(passd)
        new_user.user_role = request.POST.get('user_role')

        new_user.save()

        content = {
            'mssg':"User Created" 
        }
        return render (request, 'sign_up.html', content)

    return render (request, 'sign_up.html')

def logout(request):

    # Clearing session variables
    var_list = list(request.session.keys())
    for key in var_list:
        print (key,request.session[key])
        del request.session[key]
    return redirect('index')
 

def index(request):
    if 'user_role'  in request.session.keys():
        content = { 'user': request.session['user_role']}
    content ={'user':''}
    return render(request,'index.html', content)


def appointments(request):
    return render(request,'appointments.html')


def profile(request):
    email = request.session['email']
    _id = request.session['id']
    login_user = user.objects.filter(id=_id).first()
    print (login_user.email)
    content = {
        'user':login_user
    }
    return render(request,'user_profile.html', content)


def inner(request):
    # return HttpResponse("Hello, world.")
    return render(request,'inner-page.html')

@doctor_logged_in
def news (request):
    news = scraped_data.objects.all()
    content = {
        'data': news
    }
    print (content)
    return render(request,'news.html', content)




def fetch_news(request):
    import modules.scrape_final

    # return HttpResponse("News fetched")
    return render(request,'news_fetched.html')


def data_extract(request):
    import modules.report_extraction_final

    return HttpResponse("Report Data obtained")

@receptionist_logged_in
def report (request):
    rep = reports.objects.all()
    # rep = json.dumps(rep)
    # print (rep.normal)
    content = { 
        'data': rep
    }
    print (content['data'])

    # normal = content['data'][0].normal
    
    # normal = json.dumps (normal)
    # normal = json.loads(normal)
    # print (type(normal))
    # print (normal['Haemoglobin'])
    # json.dumps (content['data'])
    # https://www.geeksforgeeks.org/python-convert-dictionary-to-list-of-tuples/

    return render(request,'reports.html', content)

@doctor_logged_in
def single_report (request, param):

    rep = reports.objects.filter(id=param).first()
    content = { 
        'data': rep
    }
    print (content['data'])

    return render(request,'single_report.html', content)

@receptionist_logged_in
def patient_add(request):
    if request.method == "POST":
        if request.POST.get('name') and request.POST.get('gender') and request.POST.get('age') and request.POST.get('birthday') and request.POST.get('email') and request.POST.get('address') and request.POST.get('pincode'):
            
            filename='/media/patients/default.jpeg'
            try:
                file = request.FILES['img']
                # if file and allowed_file(file.name):
                storage = FileSystemStorage(location=BASE_DIR+'/media/patients') 
                url = storage.save(file.name, file)
                filename = '/media/patients/'+url
            except Exception as e:
                print("Form without file " + str(e)) 
            print (filename)

            saverecord = patient()
            saverecord.name = request.POST.get('name')
            saverecord.gender = request.POST.get('gender')
            saverecord.age = request.POST.get('age')
            saverecord.birthday = request.POST.get('birthday')
            saverecord.email = request.POST.get('email')
            saverecord.phone = request.POST.get('phone')
            saverecord.address = request.POST.get('address')
            saverecord.pincode = request.POST.get('pincode')
            saverecord.imgpath = filename
            saverecord.save()
            messages.success(request,'Record Saved')

            content = {
            'mssg':"Patient Added to directory" 
            }
            return render(request,'patient_addinfo.html', content)
    else :
        return render(request,'patient_addinfo.html')
#adding appointment
# def addappoint(request):
#     context = {"time_slot": ['9:00','9:20','9:40','10:00','10:20','10:40']}  
#     # athlete_list=['9:00','9:20','9:40','10:00','10:20','10:40']
#     if request.method == 'POST':
#         date = request.POST.get('datepicker')
#         print(date)
#         request.session['date'] = date
#         return redirect  ('time_slot', date)


#     return render(request,'addappoint.html',context)

# def time_slot(request):
#     print (param)

#     test = request.session['date']
#     print ('sakuuuu', test)
#     return render(request,'time_slot.html')


def get_daily_slots(start, end, slot, date):
    # combine start time to respective day
    dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
    slots = [dt]
    # increment current time by slot till the end time
    while (dt.time() < datetime.strptime(end,"%H:%M").time()):
        dt = dt + timedelta(minutes=slot)
        slots.append(dt)
    return slots

# Some Dummy values 
start_time = '9:00'
end_time = '15:00'
slot_time = 20
days = 7
start_date = datetime.now().date()

unavailable_slot=[]
for i in range(days):
    date_required = datetime.now().date() + timedelta(i)
    list_date_available = get_daily_slots(start=start_time, end=end_time, slot=slot_time, date=date_required)
    # print (get_daily_slots(start=start_time, end=end_time, slot=slot_time, date=date_requir
print(list_date_available)
def time_slot(request,param):
    avail=[]
    year=int(param[0:4])
    month=int(param[5:7])
    day=int(param[8:10])
    print(type(year))
    print(list_date_available)
    for i in list_date_available:
        if year == i.year and month == i.month and day == i.day:
           avail.append(str(i.hour)+':'+str(i.minute))
    context={"timeslot":avail}
    if request.method == 'POST':
        print(param)
        time_taken=request.POST.get('dropdown')
        hour=int(time_taken[0:2])
        minute=int(time_taken[3:])
        print(time_taken)
        if request.POST.get('patient_id') and request.POST.get('mobile') and request.POST.get('dropdown'):
            print('patient')
            saverecord = appointment()
            saverecord.patient_id = request.POST.get('patient_id')
            saverecord.date = param
            saverecord.mobile = request.POST.get('mobile')
            saverecord.timeslot = request.POST.get('dropdown')
            saverecord.save()
            messages.success(request,'Record Saved')
        for i in list_date_available:
            if i.year == year and i.month== month and i.day== day and i.hour==hour  and i.minute == minute:
                    list_date_available.remove(i)
    return render(request,'time_slot.html',context)




def addappoint(request):
    # context = {"time_slot": ['9:00','9:20','9:40','10:00','10:20','10:40']}  
    # athlete_list=['9:00','9:20','9:40','10:00','10:20','10:40']
    if request.method == 'POST':
        date = request.POST.get('datepicker')
        print(date)
        request.session['date'] = date
        return redirect  ('time_slot', date)
    return render(request,'addappoint.html')




@doctor_logged_in
def patient_information (request):
    
    pat = patient.objects.first()
    if pat == None:
        pass # condition for entering first entry
    print (pat.name)
    pats = patient.objects.all()
    report = reports.objects.filter(name=pat.name).first()
    
    if request.method == "POST":
        PatientName = request.POST.get('patientName')
        print (PatientName)
        pat = patient.objects.filter(name=PatientName).first()
        report = reports.objects.filter(name=PatientName)

    print (pat.name)
    content = {
        'data': pat,
        'pats': pats,
        'reports': report
    }
    print (content['reports'])
    return render(request,'patient_info.html', content)

@receptionist_logged_in
def report_upload(request):
    if request.method == 'POST' and request.FILES['report']:
        try:
            file = request.FILES['report']
            # if file and allowed_file(file.name):
            #     print ('work')
                # attachment_file = secure_filename(file.filename)
            storage = FileSystemStorage(location=BASE_DIR+'/media/reports')
            url = storage.save(file.name, file)
            print (url)
            report_extraction_final.main(url)
            return render(request, 'report_upload.html', {
            'uploaded_file_url': url
            })

        except Exception as e:
            print("Form without file " + str(e))

    return render(request, 'report_upload.html')



def broadcast_sms(request):
    date_time='3 September 2020, 11:00am'
    message_to_broadcast = ("Your Appointment is Scheduled at:"+date_time)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # recipient = '+918898630781'
    # recipient = '+917506454404'
    # recipient = '+918275510613'

    #  for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
    #     if recipient:
    client.messages.create(to=recipient,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)

@doctor_logged_in
def prescription(request):
    # return HttpResponse("Hello, world.")
    return render(request,'prescription.html')


############################## User roles

"""
def registerPage(request):
    
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

"""

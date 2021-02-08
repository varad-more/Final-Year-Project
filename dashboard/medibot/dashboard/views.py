from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

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
        print ('POST')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        print (email)
        print (password)
        # print ()
        # entered_key = hash_password(password)
        login_user = user.objects.filter(email=email, password=password).first()
        print (login_user)
        if login_user:
            print(login_user.user_role,'000000')
            request.session['user_role'] = login_user.user_role
        
        else:

            print('Bad Credentials')
            content = {'error': 'Password Incorrect'}
            return render (request, 'sign_in.html', content)

    return render (request, 'sign_in.html')

def sign_up(request):

    print ('sign up')
    if request.method == 'POST' :
        print ('post')
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        user_role = request.POST.get('user_role')

        print (password)
        print (email)
        print (user_role)
        print (gender)

        new_user = user()
        new_user.name = request.POST.get('name')
        new_user.email = request.POST.get('email')
        new_user.age = request.POST.get('age')
        new_user.gender = request.POST.get('gender')
        new_user.phone = request.POST.get('phone')
        new_user.password = request.POST.get('pass')
        new_user.user_role = request.POST.get('user_role')

        new_user.save()

        content = {
            'mssg':"User Saved" 
        }
        return render (request, 'sign_up.html', content)

    return render (request, 'sign_up.html')

 

def index(request):
    # return HttpResponse("Hello, world.")
    return render(request,'index.html')


def appointments(request):
    # return HttpResponse("Hello, world.")
    return render(request,'appointments.html')

def inner(request):
    # return HttpResponse("Hello, world.")
    return render(request,'inner-page.html')

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


def report (request):
    # return HttpResponse("Hello, world.")
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

def single_report (request, param):

    rep = reports.objects.filter(id=param).first()
    # rep = reports.objects.filter(name=param)

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

    return render(request,'single_report.html', content)


# @login_required(login_url='login')
# @admin_only
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
            return render(request,'patient_addinfo.html')
    else :
        return render(request,'patient_addinfo.html')

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



############################## User roles

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

def prescription(request):
    # return HttpResponse("Hello, world.")
    return render(request,'prescription.html')
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

def logoutUser(request):
	logout(request)
	return redirect('login')

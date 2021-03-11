from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from datetime import datetime,timedelta

from contextlib import contextmanager
#Twilio - SMS Module
from twilio.rest import Client
from django.conf import settings  

from dashboard.models import *
# from dashboard.models import patient

# Import refactored modules 
from modules import report_extraction_final, speech_recognition_google, ner_model

# from modules import *
import json

# from werkzeug.utils import secure_filename
from django.core.files.storage import FileSystemStorage 
import os
from .forms import *

from django.contrib import messages
from .decorators import doctor_logged_in,receptionist_logged_in,hash_password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
allowed_file = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4' ,''])




def sign_in(request):
    print ('signin')

    if request.method == 'POST' :
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        entered_key = hash_password(password)

        # To be hashed
        login_user = user.objects.filter(email=email, password=entered_key).first()

        print (login_user)

        if login_user:
            request.session['user_role'] = login_user.user_role
            request.session['email'] = login_user.email
            request.session['id'] = login_user.id

            return redirect ('appointments')
        
        else:

            print('Bad Credentials')
            content = {'error': 'Password Incorrect'}
            return render (request, 'sign_in.html', content)

    content={}
    if 'error'  in request.session.keys():
        content = { 'error': request.session['error']}
        del request.session['error']
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


def get_daily_slots(start, end, slot, date):
    # combine start time to respective day
    dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
    slots = [dt]
    # increment current time by slot till the end time
    while (dt.time() < datetime.strptime(end,"%H:%M").time()):
        dt = dt + timedelta(minutes=slot)
        slots.append(dt)
    return slots


def time_slot(request,param):

    # Set Appointment slot times 
    start_time = '9:00'
    end_time = '15:00'
    # Avg appointment duration
    slot_time = 20

    # days = 7
    # start_date = datetime.now().date()
    
    # fetched from database
    datetime_object_param = datetime.strptime(param, '%Y-%m-%d')
    
    date_bookings = appointment.objects.filter(date__gte =param, date__lte= datetime_object_param+timedelta(1))
    unavailable_slot=[]
    for i in date_bookings:
        print (i.date)
        unavailable_slot.append(i.date.replace(tzinfo=None))
    # print (unavailable_slot)

    date_required = datetime_object_param  
    list_date_available = get_daily_slots(start=start_time, end=end_time, slot=slot_time, date=date_required)
    
    list_date_available = [i for i in list_date_available if i not in unavailable_slot] 
    print('REST:',list_date_available)

    available_timeslots=[]
    for i in list_date_available:
           available_timeslots.append(str("{0:0>2}".format(i.hour))+':'+str("{0:0>2}".format(i.minute)))

    context={"timeslot":available_timeslots}

    if request.method == 'POST':
        time_taken=request.POST.get('dropdown')

        datetime_object = datetime.strptime(param + ' ' + str(time_taken) , '%Y-%m-%d %H:%M')
        print (datetime_object)

        if request.POST.get('patient_id') and request.POST.get('mobile') and request.POST.get('dropdown'):
            # print('patient')
            saverecord = appointment()
            saverecord.patient_id_id = request.POST.get('patient_id')
            saverecord.date = datetime_object
            saverecord.mobile = request.POST.get('mobile')
            saverecord.save()
            messages.success(request,'Record Saved')

            content = {'mssg': 'Appointment Confirmed'}
            return render(request,'addappoint.html', content)

        
    return render(request,'time_slot.html',context)




def addappoint(request):
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

def start_appointment (request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mob = request.POST.get('mob')
        row_id = request.POST.get('row_id')

        print (name,mob, row_id, '--------------')

        ongoing_appointment = appointment.objects.all()[int(row_id)-1]
        
        # Alternate query 
        # appoints = appointment.objects.filter(mobile=mob).first()

        # print (appoints[row_id-1])
        # print (type(ongoing_appointment))
        # print (ongoing_appointment)
        # print (ongoing_appointment.mobile)
    
        request.session['patient_mobile'] = ongoing_appointment.patient_id.phone
        request.session['patient_name'] = ongoing_appointment.patient_id.name
        request.session['patient_id'] = ongoing_appointment.patient_id.id
        request.session['appointment_id'] = ongoing_appointment.id

        ongoing_appointment.status = 'On going'
        ongoing_appointment.save()

    return redirect ('prescription')

def stop_appointment  (request):
    if request.method == 'POST':
        print (request.session['patient_id'])
        appointment_id = request.session['appointment_id']
        ongoing_appointment = appointment.objects.filter(id= appointment_id).first()

        ongoing_appointment.status = 'Completed'
        ongoing_appointment.save()

        var_list = ['patient_mobile', 'patient_name', 'patient_id', 'appointment_id']
        for key in var_list:
            print ('deleted:',key,request.session[key])
            del request.session[key]

        # print (request.session['patient_id'])        
    return redirect ('appointments')


def no_show_appointment (request):
    if request.method == 'POST':
        print ('post')

        # Following should be entered in the database
        # ongoing_appointment.status = 'Not appeared'
    
    return redirect ('appointments')


def appointments(request):
    
    today_date = datetime.now().date()
    print(today_date)
    tomorrow_date = datetime.now() + timedelta(days=1)

    today_appointment = appointment.objects.filter(date__gte =today_date, date__lte= tomorrow_date)
    tomorrow_appointment = appointment.objects.filter(date__gte =tomorrow_date, date__lte= datetime.now() + timedelta(days=1))

    appoints = appointment.objects.all()
    for i in appoints:
        print(i.date.strftime("%x"))
    
    content = {
        'today_apppointment':today_appointment,
        'tomorrow_appointment': tomorrow_appointment
        
        
    }
    print(content)
    #{'databasename':function-name}
    return render(request,'new_appointment.html',content)


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


# @doctor_logged_in
def prescription(request):
    content = {}
    if request.method == 'POST':

        patient_name = request.session['patient_name']

        file_name = patient_name

        f = open(BASE_DIR+'/media/recordings/'+file_name+'.wav', 'wb')
        f.write(request.body)
        f.close()
        

        file_loc = BASE_DIR+'/media/recordings/'+file_name+'.wav'
        print (file_loc) 
        
        text_data = speech_recognition_google.split(file_loc)
        
        print ('text', text_data)

        final_output = ner_model.run_model(text_data)
        print (final_output)

        content = {'prescription':final_output['medicine']}
        # content = {'prescription':'Some Tablets!!'}

        # No repsponse is sent (needs rectification)
        # return redirect ("index")
        return render(request,'prescription_sonal.html',content)        
        # return HttpResponseRedirect('prescription')


    return render(request,'prescription_sonal.html',content)
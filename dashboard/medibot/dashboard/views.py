from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.utils import timezone

from contextlib import contextmanager
#Twilio - SMS Module
from twilio.rest import Client
from django.conf import settings  

from dashboard.models import *
# from dashboard.models import patient

# Import refactored modules 
from modules import report_extraction_final, speech_recognition_google, ner_model, mailer

# from modules import *
import json
import math

# from werkzeug.utils import secure_filename
from django.core.files.storage import FileSystemStorage 
import os
from .forms import *

from django.contrib import messages
from .decorators import doctor_logged_in,receptionist_logged_in,hash_password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
allowed_file = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4' ,''])


def sign_in(request):
    """
    Sign Method to authenticate user 
    Redirect incase of incorrect bad credentials
    """
    content={}

    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('pass')

        entered_key = hash_password(password)

        login_user = user.objects.filter(email=email, password=entered_key, verification = 'verified').first()

        print (login_user)

        if login_user:
            request.session['user_role'] = login_user.user_role
            request.session['email'] = login_user.email
            request.session['id'] = login_user.id

            if request.session['user_role'] == 'doctor':
                return redirect ('appointments')

            else:
                return redirect ('add_appointment')
                
        else:
            print('Bad Credentials')
            content = {'error': 'Password Incorrect / Complete E-mail Verification'}
            return render (request, 'sign_in.html', content)

    # For displaying occured errors to the users
    if 'error'  in request.session.keys():
        content = { 'error': request.session['error']}
        del request.session['error']
    return render (request, 'sign_in.html', content)


def sign_up(request):
    """
    To Register Users with respective user roles
    """

    if request.method == 'POST' :
        
        passd = request.POST.get('pass')
        email = request.POST.get('email')
        name = request.POST.get('name')
        # Check condition for duplicate user
        login_user = user.objects.filter(email=email).first()
        
        if login_user:
            context = {"mssg": "User Already Exists"}
            return render (request, 'sign_up.html', context)
            
        new_user = user()
        new_user.name = name 
        new_user.email = email
        new_user.age = request.POST.get('age')
        new_user.gender = request.POST.get('gender')
        new_user.phone = request.POST.get('phone')
        new_user.password = hash_password(passd)
        new_user.user_role = request.POST.get('user_role')

        new_user.save()

        mailer.send_mail(name, email)

        # Confirmation on creation of user
        request.session['error']= "User Created, Check Inbox and verify mail before login" 
        return redirect ('signin')

    return render (request, 'sign_up.html')


def logout(request):
    """
    Logout user and clear session variables
    """

    # Clearing session variables
    var_list = list(request.session.keys())
    for key in var_list:
        print (key,request.session[key])
        del request.session[key]

    return redirect('index')
 

def index(request):
    """
    Default Landing Pages 
    Checks for signed in user --> for deciding options to display in navbar
    """

    content ={'user':''}
    if 'user_role'  in request.session.keys():
        content = { 'user': request.session['user_role']}
    return render(request,'index.html', content)


def profile(request):
    """
    Yet to complete profile page for displaying user profile
    """
    email = request.session['email']
    _id = request.session['id']
    login_user = user.objects.filter(id=_id).first()
    print (login_user.email)
    content = {
        'user':login_user
    }
    return render(request,'user_profile.html', content)


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

"""
Functions of Seggrated by Roles '@' ---> Autenticated using decorators
"""


@receptionist_logged_in
def report (request):
    """
    Check all uploaded reports in bluck view
    """

    rep = reports.objects.all()
    # rep = json.dumps(rep)
    # print (rep.normal)
    content = { 
        'data': rep
    }
    print (content['data'])

    return render(request,'reports.html', content)


@doctor_logged_in
def single_report (request, param):
    """
    Individual Report of a patient displayed based on param --> unique report id
    """

    rep = reports.objects.filter(id=param).first()
    content = { 
        'data': rep
    }
    print (content['data'])

    return render(request,'single_report.html', content)


@receptionist_logged_in
def patient_add(request):
    """
    Adding new patient to the directory
    """

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
    """
    Returns Total Time slots available for a day
    """
    # combine start time to respective day
    dt = datetime.combine(date, datetime.strptime(start,"%H:%M").time())
    slots = [dt]
    # increment current time by slot till the end time
    while (dt.time() < datetime.strptime(end,"%H:%M").time()):
        dt = dt + timedelta(minutes=slot)
        slots.append(dt)
    return slots

@receptionist_logged_in
def time_slot(request,param):
    """
    Book an appointment for selected param --> date 
    """
    # Set Appointment slot times 
    start_time = '9:00'
    end_time = '15:00'
    # Avg appointment duration
    slot_time = 20

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
    
    # Removing list of booked slots from the list
    list_date_available = [i for i in list_date_available if i not in unavailable_slot] 
    print('REST:',list_date_available)

    available_timeslots=[]
    for i in list_date_available:
           available_timeslots.append(str("{0:0>2}".format(i.hour))+':'+str("{0:0>2}".format(i.minute)))
    var = request.session.get('patient_id')
    pat = patient.objects.filter(id = var).first()
    context={"timeslot":available_timeslots,"pat":pat}

    if request.method == 'POST':
        time_taken=request.POST.get('dropdown')

        datetime_object = datetime.strptime(param + ' ' + str(time_taken) , '%Y-%m-%d %H:%M')
        print (datetime_object)

        if  request.POST.get('dropdown'):
            # print('patient')
            
            saverecord = appointment()
            saverecord.patient_id_id = request.session.get('patient_id')
            saverecord.date = datetime_object
            print(pat.phone)
            saverecord.mobile = pat.phone
            saverecord.save()
            messages.success(request,'Record Saved')

            request.session['mssg'] = 'Appointment Confirmed'

            return redirect ('add_appointment')
        
    return render(request,'time_slot.html',context)



@receptionist_logged_in
def add_appointment(request):
    """
    Book an Appointment --> Only Date
    """
    if request.method == 'POST':
        date = request.POST.get('datepicker')
        patient_id = request.POST.get('patient_id')
        print(date)
        request.session['date'] = date
        request.session['patient_id'] = patient_id
        return redirect  ('time_slot', date)
    content ={}    

    if 'mssg'  in request.session.keys():
        content = { 'mssg': request.session['mssg']}
        del request.session['mssg']

    return render(request,'add_appointment.html', content)




@doctor_logged_in
def patient_information (request):
    """
    Display information of ongoing appointment patient
    """

    ##condition for selection of patient
    '''
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
        history= patient_history.objects.filter(patient_id_id=pat.id)
    '''

    if 'patient_id' not in request.session.keys():
        content = {"mssg": "Select Patient First"}
        return  render (request, "new_appointment.html", content)

    
    patient_id = request.session.get('patient_id')
    print (patient_id)
    pat = patient.objects.filter(id= patient_id).first()
    report = reports.objects.filter(patient_id = pat.id)
    history= patient_history.objects.filter(patient_id_id=pat.id)

    half_list = math.ceil(len(history)/2)
 
    content = {
        'data': pat,
        # 'pats': pats,
        'reports': report,
        'history':history,   
        'half_list': half_list
    }
    print (content['reports'])
    return render(request,'patient_info.html', content)

def start_appointment (request):
    """
    Marks onset on an appointment and stores required details to session
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        mob = request.POST.get('mob')
        row_id = request.POST.get('row_id')
        appt_id = request.POST.get('appt_id')

        print (name,mob, row_id, appt_id, '--------------')
        print(appt_id)
        
        ongoing_appointment = appointment.objects.filter(id=appt_id).first()

        print(ongoing_appointment)
    
        request.session['patient_mobile'] = ongoing_appointment.patient_id.phone
        request.session['patient_name'] = ongoing_appointment.patient_id.name
        request.session['patient_id'] = ongoing_appointment.patient_id.id
        request.session['appointment_id'] = ongoing_appointment.id

        ongoing_appointment.status = 'On Going'
        ongoing_appointment.save()

    return redirect ('current_appointment')

def stop_appointment  (request):
    """
    Marks completion of appointment and clears session variables
    """
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

    return redirect ('appointments')


def no_show_appointment (request):
    """
    Marks no show the appointment incase patient misses it.
    """
    today_date = (date.today())
    tomorrow_date = date.today() + timedelta(days=1)
    if request.method == 'POST':
        appt_id = request.POST.get('appt_id')

        ongoing_appointment = appointment.objects.filter(id=appt_id).first()
        print(ongoing_appointment) 
        ongoing_appointment.status = 'No Show'
        ongoing_appointment.save()
    
    return redirect ('appointments')

@doctor_logged_in
def appointments(request):
    """
    Displays list of booked appointment date wise
    """

    today_date = (date.today())
    print(today_date)
    tomorrow_date = date.today() + timedelta(days=1)
    print(tomorrow_date)
    # appoints = appointment.objects.all()
    
    today_appointment = appointment.objects.filter(date__gte =today_date, date__lte= tomorrow_date)
    tomorrow_appointment = appointment.objects.filter(date__gte =tomorrow_date, date__lte= date.today() + timedelta(days=2))
    
    print (today_appointment, tomorrow_appointment, '))))))))))))')
    
    content = {
        'today_apppointment':today_appointment,
        'tomorrow_appointment': tomorrow_appointment        
    }
    
    if request.session.get('appointment_id') :
        content['appointment'] = 'yes' 
    return render(request,'new_appointment.html',content)


@receptionist_logged_in
def report_upload(request):
    """
    Upload reports of the patients
    """
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
    """"
    Automated function for sending SMS reminders to the patients, ran by an crontab call
    """
    
    today_date = (date.today())
    tomorrow_date = date.today() + timedelta(days=1)

    today_appointment = appointment.objects.filter(date__gte =today_date, date__lte= tomorrow_date)

    for appoint in today_appointment:
        print (appoint.patient_id.name, appoint.patient_id.phone, appoint.date)

        message_to_broadcast = (f"Hello, {appoint.patient_id.name} \n Your Appointment is Scheduled for today at: "+ str(appoint.date.strftime("%H:%M:%S")))
        print (message_to_broadcast)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        recipient = '+91'+appoint.mobile #appoint.patient_id.phone
        # recipient = '+918898630781'
        # recipient = '+917506454404'
        # recipient = '+918275510613'
        try:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)

        except Exception as e:
            print (e)

    return HttpResponse("messages sent!", 200)


@doctor_logged_in
def current_appointment(request):
    """
    Option for recording and submiting the recording for minutes
    Returns type prescription for every appointment
    """
    if 'patient_id'  not in request.session.keys():
        content = {"mssg": "Select Patient First"}
        return  render (request, "new_appointment.html", content)


    content = {}
    if request.method == 'POST':

        patient_name = request.session['patient_name']
        patient_id = request.session['patient_id']
        appointment_id = request.session['appointment_id']
        file_name = patient_name
        # file_name = 'test'

        f = open(BASE_DIR+'/media/recordings/'+file_name+'.wav', 'wb')
        f.write(request.body)
        f.close()

        file_loc = BASE_DIR+'/media/recordings/'+file_name+'.wav'
        print (file_loc) 
        
        text_data = speech_recognition_google.split(file_loc)
        
        print ('text', text_data)

        final_output = ner_model.run_model(text_data)
        print (final_output['symptom'])

        final_output['medicine'] = ner_model.run_medacy(text_data)
        p = patient_history(patient_id_id = patient_id, appointment_id_id=appointment_id, symptom = final_output['symptom'],prescription=final_output['medicine'])
        p.save()

        content = {'prescription':final_output['medicine']}
        # content = {'prescription':'Some Tablets!!'}
        # p = patient_history('symptom':'symptom')

        return HttpResponse(json.dumps(content), content_type="application/json")
        # return render(request,'current_appointment.html',content)        

    return render(request,'current_appointment.html',content)


@doctor_logged_in
def confirmed_prescription(request):
    """
    Function for updating the stored prescription
    """
    if request.method == "POST":
        conf_prescription = request.POST.get('prescription')
        print (conf_prescription)
        patient_id = request.session['patient_id']
        appointment_id = request.session['appointment_id']
        p = patient_history.objects.filter(patient_id_id = patient_id, appointment_id_id=appointment_id).first()
        p.prescription = conf_prescription 
        p.save()

    return redirect ('appointments')


def verify(request, user_id, verification_code):
    verify_profile = user.objects.filter(id=user_id, verification = verification_code).first()
    content={}
    if verify_profile:
        verify_profile.verification = 'verified'
        verify_profile.save()

        content = {
            'mssg': 'E-Mail Successfully Verified. Now you can login.'
        }

    else :
        verified_profile = user.objects.filter(id=user_id, verification = 'verified').first()

        if verified_profile:
            content = {
            'mssg': 'E-Mail is already Verified. Now you can login.'
            }

        else:
            content = {
            'mssg': "Cannot verify E-Mail, contact Admin"
            }
    return render (request, 'email_verification.html', content)
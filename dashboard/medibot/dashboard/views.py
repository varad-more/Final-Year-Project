from django.shortcuts import render, redirect
from django.http import HttpResponse

#Twilio - SMS Module
from twilio.rest import Client
from django.conf import settings  


# Create your views here.
from dashboard.models import *

#Report Uploader Module
from modules import report_extraction_final
import json
# from werkzeug.utils import secure_filename
from django.core.files.storage import FileSystemStorage 
import os
from .forms import *


allowed_file = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4' ,''])


def index(request):
    # return HttpResponse("Hello, world.")
    return render(request,'index.html')

def inner(request):
    # return HttpResponse("Hello, world.")
    return render(request,'inner-page.html')

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
    # https://www.geeksforgeeks.org/python-convert-dictionary-to-list-of-tuples/

    return render(request,'reports.html', content)

def news (request):
    news = scraped_data.objects.all()
    content = {
        'data': news
    }
    print (content)
    return render(request,'news.html', content)


def report_upload(request):
    if request.method == 'POST' and request.FILES['report']:
        try:
            file = request.FILES['report']
            # if file and allowed_file(file.name):
            #     print ('work')
                # attachment_file = secure_filename(file.filename)
            storage = FileSystemStorage(location='media/reports')
            url = storage.save(file.name, file)
            print (url)
            report_extraction_final.main(url)
            return render(request, 'report_upload.html', {
            'uploaded_file_url': url
            })

        except Exception as e:
            print("Form without file " + str(e))

    return render(request, 'report_upload.html')



# def report_upload (request):
#     if (request.method=='POST'):
#         # report_name = request.form.get('name')
#         try:
#             file = request.file['report'].read()
#             if file:  #and allowed_file(file.filename):
#                 filename = (file.name)
#                 print (filename)
#                 # file.save(os.path.join(app.config['UPLOAD_FOLDER'], "1ngo", filename))

#             else:
#                 filename = request.form.get('file')
#         except Exception as e:
#             print("Form without file " + str(e))

#         # image = str(filename)
#     return render (request,'report_upload.html')


def broadcast_sms(request):
    date_time='3 September 2020, 11:00am'
    message_to_broadcast = ("Your Appointment is Scheduled at:"+date_time)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    recipient = '+918898630781'
    # recipient = '+917506454404'
    # recipient = '+918275510613'

    #  for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
    #     if recipient:
    client.messages.create(to=recipient,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)


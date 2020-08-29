from django.shortcuts import render

# Create your views here.
from dashboard.models import reports, scraped_data

from django.http import HttpResponse
from twilio.rest import Client
from django.conf import settings  
from .forms import UploadFileForm

def index(request):
    # return HttpResponse("Hello, world.")
    return render(request,'index.html')

def report (request):
    # return HttpResponse("Hello, world.")
    rep = reports.objects.all()
    content = {
        'data': rep
    }
    print (content['data'][0].normal)
    
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

# def report(request):
#     news = scraped_data.objects.all()
#     content = {
#         'data': news
#     }
#     print (content)
#     return render(request,'reports.html', content)


def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'report_upload.html', {'form': form})


def report_upload (request):
    if (request.method=='POST'):
        # report_name = request.form.get('name')
        try:
            file = request.file['report'].read()
            if file:  #and allowed_file(file.filename):
                filename = (file.filename)
                print (filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], "1ngo", filename))

            else:
                filename = request.form.get('file')
        except Exception as e:
            print("Form without file " + str(e))

        # image = str(filename)
    return render (request,'report_upload.html')


def broadcast_sms(request):
    date_time='3 September 2020, 11:00am'
    message_to_broadcast = ("Your Appointment is Scheduled at:"+date_time)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # recipient = '+917506454404'
    # recipient = '+918275510613'
    #  for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
    #     if recipient:
    client.messages.create(to=recipient,
                           from_=settings.TWILIO_NUMBER,
                           body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)
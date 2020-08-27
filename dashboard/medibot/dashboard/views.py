from django.shortcuts import render

# Create your views here.
from dashboard.models import reports, scraped_data

from django.http import HttpResponse


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
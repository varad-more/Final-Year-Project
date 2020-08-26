from django.shortcuts import render

# Create your views here.
from dashboard.models import reports

from django.http import HttpResponse


def index(request):
    # return HttpResponse("Hello, world.")
    return render(request,'index.html')

def report(request):
    # return HttpResponse("Hello, world.")
    reports = reports.objects.all()
    print (reports)
    return render(request,'reports.html', reports)
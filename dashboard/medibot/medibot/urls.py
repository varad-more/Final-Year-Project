"""medibot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dashboard.views import *


urlpatterns = [
    # path ('admin/', admin.site.urls),
    
    # User Roles
    path ('signin', sign_in , name ='signin'),
    path ('register', sign_up , name ='signup'),
    path ('profile', profile, name ='profile'),
	path('logout', logout, name="logout"),

    # Generic functional URLs
    path ('', index , name ='index'),
    path ('sms', broadcast_sms, name="default"),
    path ('fetch',fetch_news, name = 'fetch_news'),

    # Receptionist user URLs
    path ('report',report, name='report'),
    path ('report_upload',report_upload, name='report_upload'),
    path ('add_appointment',add_appointment, name='add_appointment'),
    path ('add_patient',patient_add),
    path ('time_slot/<slug:param>',time_slot, name = 'time_slot'),

    # Doctor user URLs
    path ('single_report/<slug:param>',single_report, name='single_report'),
    path ('news',news, name='news'),
    path ('patient_information',patient_information, name = 'patient_information'),
    path ('current_appointment',current_appointment, name = 'current_appointment'),
    path ('appointments',appointments, name = 'appointments'),
    path ('confirmed_prescription', confirmed_prescription, name='confirmed_prescription'),

    # Appointment Management Features
    path ('start_appointment',start_appointment, name = 'start_appointment'),
    path ('stop_appointment',stop_appointment, name = 'stop_appointment'),
    path ('no_show_appointment',no_show_appointment, name = 'no_show_appointment')
    
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from dashboard.views import index,report,rep_generatoion,register, pdf_downloader, sec_master
from dashboard.views import *
# from .router import router


urlpatterns = [
    path ('admin/', admin.site.urls),
    path ('', index , name ='index'),
    path ('inner', inner , name ='default'),
    path ('sms', broadcast_sms, name="default"),
    path ('report_upload',report_upload, name='report_upload'),
    path ('report',report, name='report'),
    path ('single_report/<slug:param>',single_report, name='single_report'),
    path ('news',news, name='news'),
    path ('fetch',fetch_news),
    path ('report_extract',data_extract),
    path ('patient',patient_information),
    path ('addinfo',patient_add),
    
    path('register/', registerPage, name="register"),
	path('login/', loginPage, name="login"),  
	path('logout/', logoutUser, name="logout")

    
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

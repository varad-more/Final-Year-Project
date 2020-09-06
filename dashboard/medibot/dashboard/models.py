from django.db import models

# Create your models here.

class reports(models.Model):
    name = models.CharField(max_length=100,blank=True)
    gender = models.CharField(max_length=10, blank=True)
    age = models.CharField (max_length=3, blank=True)
    date = models.CharField(max_length=20, blank=True) 
    normal = models.TextField( blank=True)
    abnormal = models.TextField( blank=True)
    notes = models.TextField( blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class meta:
        db_table = "reports"

class scraped_data (models.Model):
    headline = models.CharField (max_length=500) 
    summary = models.CharField (max_length=500)
    links = models.CharField (max_length=500)
    class meta:
        db_table = "scraped_data"

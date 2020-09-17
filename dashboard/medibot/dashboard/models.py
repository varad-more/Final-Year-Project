from django.db import models

import jsonfield

# Create your models here.

class reports(models.Model):
    name = models.CharField(max_length=100,blank=True)
    gender = models.CharField(max_length=10, blank=True)
    age = models.CharField (max_length=3, blank=True)
    date = models.CharField(max_length=20, blank=True) 
    normal = jsonfield.JSONField( null=True)
    abnormal = jsonfield.JSONField( null=True)
    # notes = jsonfield.JSONField( null=True)
    file_path = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now=True)

    class meta:
        db_table = "reports"

class scraped_data (models.Model):
    headline = models.CharField (max_length=500) 
    summary = models.CharField (max_length=500)
    links = models.CharField (max_length=500)
    class meta:
        db_table = "scraped_data"

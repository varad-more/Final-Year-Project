from django.db import models

# Create your models here.

class reports(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.CharField (max_length=3)
    date = models.CharField(max_length=20) 
    normal = models.TextField()
    abnormal = models.TextField()
    notes = models.TextField()
    class meta:
        db_table = "reports"

class scraped_data (models.Model):
    headline = models.CharField (max_length=500) 
    summary = models.CharField (max_length=500)
    links = models.CharField (max_length=500)
    class meta:
        db_table = "scraped_data"

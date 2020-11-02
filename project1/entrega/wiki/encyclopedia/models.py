from django.db import models

# Create your models here.

class search(models.Model):
    title=models.CharField(max_length=100,null=True)
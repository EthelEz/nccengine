from django.db import models

# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
import uuid
import datetime

# Create your models here.

# Data set model
class DataSet(models.Model):
    # ID assigned to each uploaded data set
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for uploaded data set')

    # Model representing a data set for ML training.
    name = models.CharField(max_length=200, help_text='Enter name of training data set (e.g. Solar iradiaton data for West Africa)')

    # file will be uploaded to MEDIA_ROOT/uploads
    data_file = models.FileField(upload_to='uploads/')

    # description of data
    description = models.TextField(default='',help_text='Give a brief desccription of data set you are uploading')

    # name of response column of data
    resp_colmn = models.CharField(max_length=200, default='response', verbose_name='Response column name',
        help_text= "Enter name of reponse column in data set or make sure a column in your data set is called 'response'")

    # date data file was uploaded
    upload_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['upload_date']

    def __str__(self):
        #String for representing the DataSet Model object.
        return self.name

    def get_absolute_url(self):
        #Returns the url to access a detail record for this uploaded data set.
        return reverse('dataset-detail', args=[str(self.id)])


# Trained ML models model
class TrainedMLModel(models.Model):
    # ID assigned to each uploaded data set
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for created ML model')

    # Model representing a data set for ML training.
    name = models.CharField(max_length=200, help_text='Enter name of ML model')

    # file will be uploaded to MEDIA_ROOT/trained_models
    model_file = models.FileField(upload_to='trained_models/')

    # description of data
    description = models.TextField(default='', help_text='Say what the trained ML model does')

    # date data file was uploaded
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['creation_date']

    def __str__(self):
        #String for representing the ML Model object.
        return self.name

    def get_absolute_url(self):
        #Returns the url to access a detail record of created ML model.
        return reverse('ml_model-detail', args=[str(self.id)])


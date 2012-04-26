from django.db import models

from mongoengine import *
import datetime

class Adressbook(Document):
    firstname = StringField(max_length=200)
    Lastname = StringField(max_length=200)
    adress  = StringField(max_length=100)
    phone_no = IntField()
    email = StringField(required=True)


class BlogPost(Document):
    title = StringField(required=True)
    slug = StringField(required=True, max_length=250)
    content = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now, required=True)
    tags = ListField(StringField())    
    
# Create your models here.

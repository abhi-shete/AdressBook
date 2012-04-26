# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse 
from testapp.models import Adressbook
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
import pymongo
from mongoengine.django.auth import User
#from mongoengine import *
from django.contrib.auth.decorators import login_required, user_passes_test
from mongoengine.queryset import DoesNotExist
from django.core import mail

def is_staff(function=None, redirect_field_name=REDIRECT_FIELD_NAME,login_url=None):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def loginpage(request):
    return render_to_response('login.html')

def logoutpage(request):
    
    logout(request)
    return render_to_response('login.html')

def login_user(request):
    #import pdb; pdb.set_trace()
    try:
        state = "Please log in below..."
        #username = password = ''
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username)
            connection = user.check_password(password)
    
            print user,'user'
            if connection:
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                login(request, user)
                state = "You're successfully logged in!"
                return render_to_response('index.html',{'contact':username})
                
            else:
                state = "Your username and/or password were incorrect."
    
        return render_to_response('login.html',{'state':state})
    
    except DoesNotExist:
        return render_to_response('login.html',{'state':'User does not exist...!!!'})

def changePwdPage(request,contact=None):
    print contact,'contact'
    return render_to_response('changepassword.html',{'contact':contact},
                              context_instance=RequestContext(request))  


def changePassword(request):
    try:
        usrname = User.objects.get(username=request.POST['username'])
        connection = usrname.check_password(request.POST['oldpassword'])
        if connection:
            usrname.set_password(request.POST['newpassword'])
            usrname.save()
            return render_to_response('index.html')
        
        else:
            return render_to_response('changepassword.html',{'errormsg':'username or password is incorrect.'})
        
    except DoesNotExist:
        return render_to_response('changepassword.html',{'errormsg':'User does not exist...!!!'})

 
 
def adduserpage(request):
    return render_to_response('adduser.html')    

def adduser(request):
    username=request.POST['username']
    #lastname=request.POST['last_name']
    password=request.POST['password']
    email=request.POST['email']
    user = User.create_user(username=username,password=password,email=email)
    user.save()
    connection = mail.get_connection()
    connection.open()
    #mail.send_mail('Account creation', "You'r account is successfully created \
     #               on Address Book.",'abhijeet.shete88@gmail.com',[email])

    msg = "You'r account is successfully created on Address Book."
    frm = 'abhijeet.shete88@gmail.com'
    mesg = mail.EmailMultiAlternatives('Account creation',msg,frm,[email])
    mesg.attach_file('/home/abhijeet/Documents/Abhijeet/images.jpeg')
    mesg.send()
    connection.close()
    return render_to_response('login.html',{'state':'User created successfully ...!!'})
 
   

@login_required
def index(request,contact=None):
    print contact,'Contact'
    return render_to_response('index.html',{'contact':contact})

@login_required(login_url='/loginpage')
def addpage(request):

    return render_to_response('add.html',context_instance=RequestContext(request))
    
def addEntry(request):
   
    form = Adressbook(firstname=request.POST['firstname'], 
                       Lastname=request.POST['Lastname'],
                       adress=request.POST['adress'],
                       phone_no=request.POST['phone_no'],  
                       email=request.POST['email'])
    form.save()
    return render_to_response('show.html',{'value':'Data added successfully.'},
                              context_instance=RequestContext(request))    
    
@login_required(login_url='/loginpage')    
def display(request, contact=None):
    if contact is None:
        rcordlist=Adressbook.objects.all().order_by("firstname")
        return render_to_response('display.html',{'rcordlist':rcordlist},
                        context_instance=RequestContext(request))
    else:
        rcordlist=Adressbook.objects.filter(firstname=contact)
        return render_to_response('display.html',{'rcordlist':rcordlist},
                        context_instance=RequestContext(request))
@is_staff(login_url='/staff')        
@login_required(login_url='/loginpage')
def update(request, contact=None):     
    
    rcordlist=Adressbook.objects.filter(firstname=contact)
   
    return render_to_response('update.html',{'rcordlist':rcordlist,
                                            'contact':contact},
                                    context_instance=RequestContext(request))
    
def staff_auth(request):
    
    return render_to_response('show.html',
                              {'value':'You do not have permission to modify data.'},
                              context_instance=RequestContext(request))
    
    
@login_required(login_url='/loginpage')
def show(request):

    return render_to_response('show.html',context_instance=RequestContext(request))
     

@login_required(login_url='/loginpage')    
def editpage(request,contact=None):
    if contact is None:
        return render_to_response('edit.html',context_instance=RequestContext(request))     
    else:
        p=Adressbook.objects.filter(firstname=contact)
        p=p[0]
        return render_to_response('edit.html',{'p':p,'contact':contact},
                                  context_instance=RequestContext(request)) 

  
def edit(request,contact=None):
    
    #print contact    
    p1 = Adressbook.objects.filter(firstname=contact)
    rlist = ['firstname','Lastname','adress','phone_no','email']
    
    if len(p1) != 0:
        if request.method=='POST':
          p2 = p1[0]  
          nlist = []
        
          for rc in rlist:
            nlist.append(p2[rc])
          
          i=0
          for record in rlist:     
            if record != 'Lastname' and request.POST[record]:                     
                p2[record] = request.POST[record]
                
            elif record == 'Lastname' and request.POST['lastname']:
                p2[record] = request.POST['lastname'] 
                
            else:
                p2[record] = nlist[i]  
                print p2[record]
            i=i+1
          p2.save()       
                   
          rcordlist=Adressbook.objects.filter(firstname=request.POST['firstname'])
          return render_to_response('update.html',{'rcordlist':rcordlist,
                                                    'contact':request.POST['firstname']},
                                                context_instance=RequestContext(request))
        
    else:
        return render_to_response('edit.html',{'errormsg':'Enter first name correctly'},
                    context_instance=RequestContext(request))  
    
@login_required(login_url='/loginpage')   
def deletepage(request):

    return render_to_response('delete.html',context_instance=RequestContext(request))     
     
def delete(request,contact=None):
    
    if contact is None:
        p = request.POST.get('firstname')
        p2 = Adressbook.objects.filter(firstname=p)  
        p2.delete()
        rcordlist=Adressbook.objects.all().order_by("firstname")   
        return render_to_response('display.html',{'rcordlist':rcordlist},
                                context_instance=RequestContext(request))
                                
    else:
        p = Adressbook.objects.filter(firstname=contact)    
        p.delete()
        return render_to_response('show.html',{'value':'Data deleted successfully.'},
                                context_instance=RequestContext(request))   

@login_required(login_url='/loginpage')
def searchpage(request):
    
    return render_to_response('search.html',context_instance=RequestContext(request))
    
    
def search(request):

    p = request.POST.get('firstname')
    p1 = Adressbook.objects.filter(firstname=p)
    if len(p1) != 0:
        rcordlist = p1.values_list()
        return render_to_response('update.html',{'rcordlist':rcordlist,'contact':p},
        context_instance=RequestContext(request))
        
    else:
        return render_to_response('search.html',{'errormsg':'Enter first name correctly'},
                                    context_instance=RequestContext(request))  
        
    
   

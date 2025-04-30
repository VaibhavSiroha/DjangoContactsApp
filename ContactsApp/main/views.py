from django.shortcuts import render
from .models import Contact
# Create your views here.
def home(request):
    Contacts = Contact.objects.all()
    context={'Contacts':Contacts}
    return render(request,'main/home.html',context)

def contact(request):
    return render(request,'main/contact.html')

def ContactBar(request):
    Contacts = Contact.objects.all()
    context={'Contacts':Contacts}
    return render(request,context)

def AddContact(request):
    context={}
    return render(request,'main/add-contact.html',context)

def Filter(request):
    context={}
    return render(request,'main/filter.html',context)

from django.shortcuts import render
from .models import Contact
# Create your views here.
def home(request):
    Contacts = Contact.objects.all()
    context={'Contacts':Contacts}
    return render(request,'home.html',context)

def contact(request):
    return render(request,'contact.html')

def ContactBar(request):
    Contacts = Contact.objects.all()
    context={'Contacts':Contacts}
    return render(request,context)
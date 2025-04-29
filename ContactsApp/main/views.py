from django.shortcuts import render
from .models import Contact
# Create your views here.
def home(request):
    return render(request,'home.html')

def contact(request):
    return render(request,'contact.html')

def ContactBar(request):
    names = Contact.objects.all()
    context={'names':names}
    return render(request,context)
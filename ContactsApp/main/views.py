from django.shortcuts import render,redirect
from .models import Contact
from .forms import ContactForm
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
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=ContactForm()

    context={'form':form}
    return render(request,'main/add_contact.html',context)

def Filter(request):
    context={}
    return render(request,'main/filter.html',context)

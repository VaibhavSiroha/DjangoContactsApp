from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Contact
from .forms import ContactForm,EditForm
from django.contrib.auth.decorators import login_required

def home(request):
    query = request.GET.get('q','')
    if query:
        contacts = Contact.objects.filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(number__icontains=query)
        )
    else:
        contacts = Contact.objects.all()

    context = {'Contacts': contacts, 'query': query}
    return render(request, 'main/home.html', context)


def contact(request,id):
    contact=Contact.objects.get(id=id)
    context={'contact':contact}
    return render(request,'main/contact.html',context)

def ContactBar(request):
    Contacts = Contact.objects.all()
    context={'Contacts':Contacts}
    return render(request,context)

@login_required
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

@login_required
def EditContact(request,id):
    contact=Contact.objects.get(id=id)
    if request.method=='POST':
        form=EditForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=EditForm(instance=contact)
    context={'form':form}
    return render(request,'main/edit_contact.html',context)



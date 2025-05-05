from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Contact
from .forms import ContactForm,EditForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

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

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    context={'form': form}
    return render(request, 'main/register.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
    else:
        error_message = None

    context = {'error_message': error_message}
    return render(request, 'registration/login.html', context)



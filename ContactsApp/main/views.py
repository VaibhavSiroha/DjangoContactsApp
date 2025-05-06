from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import Contact
from .forms import ContactForm,EditForm,CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

def home(request):
    query = request.GET.get('q', '')
    if request.user.is_authenticated:
        if query:
            contacts = Contact.objects.filter(
                Q(name__icontains=query) | Q(email__icontains=query) | Q(number__icontains=query),
                user=request.user 
            )
        else:
            contacts = Contact.objects.filter(user=request.user)  # Show only the user's contacts
    else:
        contacts = []

    context = {'Contacts': contacts, 'query': query}
    return render(request, 'main/home.html', context)

def contact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    context = {'contact': contact}
    return render(request, 'main/contact.html', context)

def ContactBar(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user)
        context = {'contacts': contacts}
        return render(request, 'main/contact_bar.html', context)
    else:
        return redirect('login')
    
@login_required
def AddContact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('home')
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'main/add_contact.html', context)

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



def logout_view(request):
    logout(request)
    return redirect('login')
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import random

from .models import Contact, CustomUser, Otp
from .forms import ContactForm, EditForm, CustomUserCreationForm,OtpForm

# Home + Contact Views
def home(request):
    query = request.GET.get('q', '')
    if request.user.is_authenticated:
        if query:
            contacts = Contact.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(number__icontains=query),
                user=request.user
            )
        else:
            contacts = Contact.objects.filter(user=request.user)
    else:
        contacts = []
    return render(request, 'main/home.html', {'Contacts': contacts, 'query': query})

def contact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    return render(request, 'main/contact.html', {'contact': contact})

def ContactBar(request):
    if request.user.is_authenticated:
        contacts = Contact.objects.filter(user=request.user)
        return render(request, 'main/contact_bar.html', {'contacts': contacts})
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
    return render(request, 'main/add_contact.html', {'form': form})

@login_required
def EditContact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditForm(instance=contact)
    return render(request, 'main/edit_contact.html', {'form': form})

# Register with OTP
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Generate OTP
            otp_code = str(random.randint(100000, 999999))
            Otp.objects.filter(number=user.number).delete()
            Otp.objects.create(number=user.number, otp=otp_code)

            print(f"[REGISTER OTP] For {user.number} => {otp_code}")

            # Store user ID for OTP verification
            request.session['pre_otp_user_id'] = user.id

            return redirect('verify-otp')
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/register.html', {'form': form})

# Login with OTP
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate OTP
            otp_code = str(random.randint(100000, 999999))
            Otp.objects.filter(number=user.number).delete()
            Otp.objects.create(number=user.number, otp=otp_code)

            print(f"[LOGIN OTP] For {user.number} => {otp_code}")

            request.session['pre_otp_user_id'] = user.id
            return redirect('verify-otp')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')

# OTP Verification View

def verify_otp_view(request):
    if request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            user_id = request.session.get('pre_otp_user_id')

            if not user_id:
                return redirect('login')

            user = get_object_or_404(CustomUser, id=user_id)

            try:
                otp_entry = Otp.objects.get(number=user.number)
            except Otp.DoesNotExist:
                return render(request, 'main/verify_otp.html', {'form': form, 'error': 'OTP not found'})

            if timezone.now() > otp_entry.gtime + timedelta(minutes=5):
                otp_entry.delete()
                return render(request, 'main/verify_otp.html', {'form': form, 'error': 'OTP expired'})

            if otp_entry.otp != entered_otp:
                return render(request, 'main/verify_otp.html', {'form': form, 'error': 'Incorrect OTP'})

            # OTP valid, mark verified and log in
            user.is_verified = True
            user.save()

            login(request, user)
            del request.session['pre_otp_user_id']
            otp_entry.delete()

            return redirect('home')
    else:
        form = OtpForm()

    return render(request, 'main/verify_otp.html', {'form': form})
# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

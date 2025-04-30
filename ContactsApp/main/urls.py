from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('addcontact/',views.AddContact,name='addcontact'),
    path('Filter/',views.Filter,name='filter'),
    
] 
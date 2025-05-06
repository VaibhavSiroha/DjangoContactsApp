from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/<str:id>/',views.contact,name='contact'),
    path('addcontact/',views.AddContact,name='addcontact'),
    #path('Filter/',views.Filter,name='filter'),
    path('EditPage/<str:id>',views.EditContact,name='editcontact'),
    path('register/', views.register, name='register'),  # Add registration URL
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
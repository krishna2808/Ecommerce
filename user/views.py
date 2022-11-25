from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .admin import UserCreationForm
from user.forms import UserLogin, UserProfile
from django.contrib.auth import authenticate, login, logout 
from user.models import User 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.


def account(request):
     signin_form  = UserLogin()
     signup_form  = UserCreationForm() 
     if request.method == 'POST':

          if request.POST.get('name'):
               signup_form  = UserCreationForm(request.POST)
               if signup_form.is_valid():
                    name = signup_form.cleaned_data.get('name')
                    email = signup_form.cleaned_data.get('email')
                    password = signup_form.cleaned_data.get('password')
                    User.objects.create_user(email=email, name=name, password=password).save() 
                    messages.success(request, 'Your Account Successfully Created !!! ')
                    return  HttpResponseRedirect(reverse('sign_in'))
                    
          else: 
               signin_form  = UserLogin(request.POST)
               if signin_form.is_valid():
                    email = signin_form.cleaned_data.get('email')
                    password = signin_form.cleaned_data.get('password')
                    user = authenticate(request, email=email , password=password)
                    if user is not None: 
                       login(request, user)  
                    #    messages.success(request, 'Your Account Successfully Created !!! ')
                       return  HttpResponseRedirect(reverse('dashboard'))
                    #   return HttpResponseRedirect('/dashboard') 
                       
     context = {'title' : 'Account Opening',
                'signin_form' : signin_form,
                'signup_form' : signup_form
               }                 
     return render(request, 'user/account.html', context=context)



@login_required(login_url='sign_in')
def profile(request):
    title = 'Profile'
    user = User.objects.get(email=request.user)
   
    
    if request.method == 'POST': 
     #    user.user_about =  request.POST.get('user_about')
        user.mobile_number = request.POST.get('mobile_number')
        user.address = request.POST.get('address')
        user.mobile_number = request.POST.get('mobile_number')
        if len(request.FILES) != 0 :
            user.pic = request.FILES['pic']
        user.save()
        messages.success(request, 'Your Profile Successfully Updated !!! ')
    initial_content = {  'email': user.email, 'name': user.name,  'address' :  user.address, 'mobile_number': user.mobile_number  }
    form = UserProfile(initial=initial_content)    
       
    return render(request, 'user/profile.html', {'form': form , 'title' : title, 'user': user})


@login_required(login_url='sign_in')
def log_out(request):
     logout(request)
     return HttpResponseRedirect(reverse('sign_in'))



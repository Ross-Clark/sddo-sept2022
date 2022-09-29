from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from user.models import User

from user.forms import CustomUserCreationForm, UpdateUserForm

import logging

logger = logging.getLogger(__name__)

class LogoutView(View):

    def get(self, request):
        
        # default logout function   
        logout(request)
        # return to login form
        return redirect('/')


class SignUpView(View):

    template_name = 'registration/signup.html'

    def get(self, request):
        
        #initialise form
        form = CustomUserCreationForm()

        return render(request,self.template_name,{'form':form})

    def post(self, request):

        #post form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
        else:
            return render(request,self.template_name,{'form':form})

        return redirect('/choose-your-own-device/')


class ProfileView(View):

    template_name = 'registration/profile.html'

    def get(self, request):

        # user data given in request

        return render(request,self.template_name)


class EditUserView(View):

    template_name = 'registration/edit_user.html'

    def get(self, request):
        
        # get user data to populate form

        try:
            un = request.user.username
            user = User.objects.get(username=un)
        except User.DoesNotExist:
            if un.contains('\r\n') or un.contains('\n'):
                un = un.replace('\r\n','').replace('\n','')
                logger.warning("User %s attempting CLRF injection",un) ####
            else:
                logger.warning("User %s not found in the database",un) ####
        
        data = {"username":user.username,"first_name":user.first_name,"last_name":user.last_name,"email":user.email,}

        form = UpdateUserForm(initial=data)

        return render(request,self.template_name,{"form":form})

    def post(self, request):

        # update user data based on form entry

        form = UpdateUserForm(data=request.POST,instance=request.user)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
        else:
            return render(request,self.template_name,{'form':form})

        return redirect('/user/profile')
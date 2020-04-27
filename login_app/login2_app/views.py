from django.shortcuts import render
from login2_app.forms import UserProfileForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def registerform(request):
    register1 = False

    if request.method == "POST":
        userform = UserProfileForm(data = request.POST)
        profileform = UserProfileInfoForm(data = request.POST)

        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password = (user.password)
            user.save()

            profile = profileform.save(commit = False)
            profile.user = user

            if 'profilepic' in request.FILES:
                profile.profilepic = request.FILES['profilepic']
            profile.save()
            register1 = True
        else:
            print(userform.errors, profileform.errors)
    else:
        userform = UserProfileForm()
        profileform = UserProfileInfoForm()
    return render(request, 'register.html', {'userform' : userform, 'profileform' : profileform, 'register1' : register1})


@login_required
def special(request):
    return HttpResponse('You are logged in, Perfect')

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active!")
        else:
            print('Someone Try to login')
            return HttpResponse('Invalid Response')
    else:
        return render(request, 'login.html', {})







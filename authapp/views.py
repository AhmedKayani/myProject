from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from .forms import UserProfileForm

from .models import UserProfile

# For the pie chart
import matplotlib.pyplot as plt
import io
import urllib, base64

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# For exceptional Handling
import traceback

# Auth keeps unsigned in users from accessing the profile view
# Guest keeps signed in users from accessing the signup and login views
from .middlewares import auth, guest

# View for the sign up page
@guest
def signup_view(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('user_profile')
        else:
            form = UserCreationForm()
    except Exception as e:
        print("An error occurred during signup:")
        print(traceback.format_exc())
        form = UserCreationForm()
    return render(request, 'authapp/signup.html', {'form': form})

# View for the login page
@guest
def login_view(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('user_profile')
        else:
            form = AuthenticationForm()
    except Exception as e:
        print("An error occurred during login:")
        print(traceback.format_exc())
        form = AuthenticationForm()
    return render(request, 'authapp/login.html', {'form': form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')

# View for the user profile page
@auth
def user_profile_view(request):
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm()

    profiles = UserProfile.objects.all()

    # Pie chart
    # All the names of the profiles
    names = [profile.name for profile in profiles]

    # All the networths of the profiles
    networths = [profile.networth for profile in profiles]

    # Settings to make the pie chart look good
    fig, ax = plt.subplots()
    ax.pie(networths, labels=names, autopct='%1.1f%%', startangle=90)

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')  

    # Save the pie chart to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    
    return render(request, 'authapp/user_profile.html', {'form': form, 'profiles': profiles,  'data': uri})

# View for the update profile page
def update_profile(request, profile_id):
    # Get the profile whose button is clicked
    profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'authapp/update_profile.html', {'form': form, 'profile': profile})

# View for deleting users
def delete_profile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        profile.delete()
        return redirect('user_profile')
    return render(request, 'authapp/delete_profile.html', {'profile': profile})
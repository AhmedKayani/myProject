from django.shortcuts import render, redirect, get_object_or_404

# Decorator for the login and home page
from .middlewares import auth, guest

# For the views of sign up and login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Forms for the user signup, login and the home page
from .forms import LoginForm, CrudForm 

# For CRUD operations without page refresh
from django.http import JsonResponse

# For the chartjs Pie chart data
import json

# For exceptional Handling
import traceback

# For the WebSocket notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# For the form of the home page
from .models import Crud, Notification

# For Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# View for the sign up page
@guest
def signup_view(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
    except Exception as e:
        print("An error occurred during signup:")
        print(traceback.format_exc())
        form = UserCreationForm()
    return render(request, 'crudApp/signup.html', {'form': form})

# View for the login page
@guest
def login_view(request):
    error_message = False
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('home')
            else:
                error_message = True
        else:
            form = AuthenticationForm()
    except Exception as e:
        print("An error occurred during login:")
        print(traceback.format_exc())
        form = AuthenticationForm()
    return render(request, 'crudApp/login.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')

# View for the user profile page
@auth
def home_view(request):
    if request.method == 'POST':
        form = CrudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CrudForm()

    profiles = Crud.objects.all()
    notifications = Notification.objects.all().order_by('-timestamp')[0]
    names = [profile.name for profile in profiles]
    networths = [float(profile.networth) for profile in profiles]

    data = {
        'labels': names,
        'datasets': [{
            'data': networths,
            'backgroundColor': [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#4BC0C0',
                '#9966FF',
                '#FF9F40',
                '#FFCD56'
            ],
        }]
    }

    return render(request, 'crudApp/home.html', {
        'form': form,
        'profiles': profiles,
        'notifications': notifications,
        'chart_data': json.dumps(data)
    })

# View for the update profile page
@auth
def update_home(request, profile_id):
    # Get the profile whose button is clicked
    profile = get_object_or_404(Crud, id=profile_id)
    if request.method == 'POST':
        form = CrudForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CrudForm(instance=profile)
    return render(request, 'crudApp/update_home.html', {'form': form, 'profile': profile})

# View for deleting users
@auth
def delete_home(request, profile_id):
    profile = get_object_or_404(Crud, id=profile_id)
    if request.method == 'POST':
        profile.delete()
        return redirect('home')
    return render(request, 'crudApp/delete_home.html', {'profile': profile})

# View for the notifications page
@auth
def notifications_view(request):
    notifications = Notification.objects.all().order_by('-timestamp')

    # Get the page number
    page_number = request.GET.get('page', 1)

    # Pagination showing 10 items par page
    paginator = Paginator(notifications, 10)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    # Get the page number
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'crudApp/notifications.html', {'page_obj': page_obj})
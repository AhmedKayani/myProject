from django.shortcuts import redirect

def redirect_to_app(request):
    return redirect('/login') # Redirecting to the home page of crudApp
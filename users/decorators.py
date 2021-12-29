from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('page')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def unauthenticated_user_HVN(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard", campainID = 4)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
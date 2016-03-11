from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth import login
from django.contrib.auth import logout


def login_user(request):
    logout(request)
    form = AuthenticationForm(None, request.POST or None)
    form.fields['username'].widget.attrs['class'] = "mdl-textfield__input"
    form.fields['username'].widget.attrs['required'] = True
    form.fields['password'].widget.attrs['class'] = "mdl-textfield__input"
    form.fields['password'].widget.attrs['required'] = True

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/status/')
    csrf(request)

    return render(request, 'login/login.html', locals())

def logout_user(request):
    logout(request)
    return redirect('/login')

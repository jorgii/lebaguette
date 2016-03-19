from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


from .forms import UserForm
from lebaguette.settings import LOGIN_REDIRECT_URL


def login_user(request):
    if request.user.is_authenticated():
        return redirect(LOGIN_REDIRECT_URL)

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
                    return redirect(LOGIN_REDIRECT_URL)
    csrf(request)

    return render(request, 'login/login.html', locals())


def logout_user(request):
    logout(request)
    return redirect('/login/')


@login_required
def edit_user(request):
    user = request.user
    user_change_form = UserForm(request.POST or None, instance=request.user)
    password_change_form = PasswordChangeForm(user=request.user,
                                              data=request.POST or None)
    if not(password_change_form.has_changed()):
        password_change_form.errors.clear()
    user_change_form.fields['username'].widget.attrs['class'] = \
        "mdl-textfield__input"
    user_change_form.fields['first_name'].widget.attrs['class'] = \
        "mdl-textfield__input"
    user_change_form.fields['last_name'].widget.attrs['class'] = \
        "mdl-textfield__input"
    user_change_form.fields['email'].widget.attrs['class'] = \
        "mdl-textfield__input"
    password_change_form.fields['old_password'].widget.attrs['class'] = \
        "mdl-textfield__input"
    password_change_form.fields['new_password1'].widget.attrs['class'] = \
        "mdl-textfield__input"
    password_change_form.fields['new_password2'].widget.attrs['class'] = \
        "mdl-textfield__input"
    if request.method == 'POST':
        if user_change_form.is_valid():
            user_change_form.save()
        if password_change_form.has_changed() and \
                password_change_form.is_valid():
            password_change_form.save()
    csrf(request)
    return render(request, 'profile/profile.html', locals())

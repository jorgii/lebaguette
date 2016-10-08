import os

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .forms import UserForm, ServerMessageForm
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm
from .models import ServerMessage


def login_user(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = CustomAuthenticationForm(None, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'login.html', locals())


def logout_user(request):
    logout(request)
    return redirect('/login/')


@login_required
def edit_user(request):
    user = request.user
    user_change_form = UserForm(request.POST or None, instance=request.user)
    password_change_form = CustomPasswordChangeForm(
        user=request.user,
        data=request.POST or None)
    if not(password_change_form.has_changed()):
        password_change_form.errors.clear()
    if request.method == 'POST':
        if user_change_form.is_valid():
            user_change_form.save()
        if password_change_form.has_changed() and \
                password_change_form.is_valid():
            password_change_form.save()
    return render(request, 'profile.html', locals())


@login_required
def home_page(request):
    try:
        latest_message = ServerMessage.objects.\
            latest('datetime_created').message
    except ObjectDoesNotExist:
        latest_message = "No message has been added yet!"
    if request.user.is_staff:
        message_form = ServerMessageForm(request.POST or None)
        message_form.fields['message'].widget.attrs['class'] = \
            "mdl-textfield__input"
        message_form.fields['message'].widget.attrs['type'] = \
            "text"
        message_form.fields['message'].widget.attrs['rows'] = \
            "5"
        if request.method == 'POST':
            if message_form.is_valid():
                message_form.save()
                return redirect('/')
    return render(request, 'home.html', locals())


@login_required
def log_page(request):
    log_path = os.path.join(settings.BASE_DIR, 'log/')
    log_files = os.listdir(log_path)
    selected_log = (request.GET.get('log') or log_files[0])
    log_file = open(log_path + '{}'.format(selected_log), 'r').read().split('message_end')
    log_result = []
    for log_file_row in log_file:
        if log_file_row != '' and log_file_row != '\n':
            log_result.append(log_file_row.split('|'))
    return render(request, 'log_page.html', locals())

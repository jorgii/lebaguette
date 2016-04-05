from django.http import HttpResponseForbidden


def is_in_group(func):
    def func_wrapper(request):
        if request.user.groups.filter(name=request.path):
            return func(request)
        else:
            return HttpResponseForbidden()
    return func_wrapper

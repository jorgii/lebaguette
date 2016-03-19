from django.http import Http404


def is_in_group(func):
    def func_wrapper(request):
        if request.user.groups.filter(name=request.path):
            return func(request)
        else:
            raise Http404
    return func_wrapper

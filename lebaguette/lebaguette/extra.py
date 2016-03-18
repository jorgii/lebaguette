from django.http import Http404


def is_in_group(group):
    def is_in_group_decorator(func):
        def func_wrapper(request):
            if request.user.groups.filter(name=group):
                return func(request)
            else:
                raise Http404
        return func_wrapper
    return is_in_group_decorator

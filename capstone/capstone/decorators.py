from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from core.models import Profile


def is_bns(function):

    def validate(request, *args, **kwargs):

        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'Barangay Nutrition Scholar':
            return function(request, *args, **kwargs)

        return HttpResponse('You are not a BNS')

    validate.__doc__ = function.__doc__
    validate.__name__ = function.__name__

    return validate


def is_nutritionist(function):

    def validate(request, *args, **kwargs):

        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'Nutritionist':
            return function(request, *args, **kwargs)

        return HttpResponse('You are not a Nutritionist')

    validate.__doc__ = function.__doc__
    validate.__name__ = function.__name__

    return validate


def is_program_coordinator(function):

    def validate(request, *args, **kwargs):

        user_type = Profile.objects.get(user=request.user).user_type
        if user_type == 'Nutrition Program Coordinator':
            return function(request, *args, **kwargs)

        return HttpResponse('You are not a Program Coordinator')

    validate.__doc__ = function.__doc__
    validate.__name__ = function.__name__

    return validate


def not_bns(function):

    def validate(request, *args, **kwargs):

        user_type = Profile.objects.get(user=request.user).user_type
        if user_type != 'Barangay Nutrition Scholar':
            return function(request, *args, **kwargs)

        return HttpResponse('You are a BNS')

    validate.__doc__ = function.__doc__
    validate.__name__ = function.__name__

    return validate
from django.http import HttpResponse
from django.shortcuts import redirect

from core.models import Profile


def redirect_to(user):

    profile = Profile.objects.get(user=user)

    if profile.user_type == 'Barangay Nutrition Scholar':
        print(profile.user_type)
        return redirect('core:bns-index')
    elif profile.user_type == 'Nutritionist':
        return redirect('core:nutritionist')
    elif profile.user_type == 'Nutrition Program Coordinator':
        pass
    else:
        pass

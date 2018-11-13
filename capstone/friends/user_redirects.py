from django.http import HttpResponse
from django.shortcuts import redirect

from core.models import Profile


def redirect_to(user):

    profile = Profile.objects.get(user=user)

    if profile.user_type == 'Barangay Nutrition Scholar':
        return redirect('core:bns_dashboard')
    elif profile.user_type == 'Nutritionist':
        return redirect('core:nutritionist')
    elif profile.user_type == 'Nutrition Program Coordinator':
        return redirect('core:program_coordinator')
    else:
        pass

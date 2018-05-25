from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View

from core.forms import UploadFileForm
from core.models import Profile
from friends import user_redirects
from datetime import datetime


class SignInView(View):

    template_name = 'core/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return user_redirects.redirect_to(request.user)
            pass
        return render(request, self.template_name, None)

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return user_redirects.redirect_to(user)

        else:
            messages.error(request, 'Invalid credentials')
            return render(request, self.template_name, None)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('core:login')


@login_required
def bns_index(request):

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'date': datetime.now(),
    }

    return render(request, 'core/bns_index.html', context)

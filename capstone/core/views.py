from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from friends.datainput import validations
from core.forms import UploadFileForm
from core.models import Profile, Notification
from datainput.models import OperationTimbang, MonthlyReweighing, FamilyProfile, FHSIS
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


def redirect_view(request):

    return redirect('core:login')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('core:login')


@login_required
def bns_index(request):

    profile = Profile.objects.get(user=request.user)

    try:
        family_profiles = FamilyProfile.objects.get(barangay=profile.barangay, date__year=datetime.now().year)
    except FamilyProfile.DoesNotExist:
        family_profiles = None


    try:
        opt = OperationTimbang.objects.get(
            barangay=profile.barangay,
            date__year=datetime.now().year
        )
    except OperationTimbang.DoesNotExist:
        opt = None

    try:
        fhsis = FHSIS.objects.get(
            barangay=profile.barangay,
            date__month=datetime.now().month
        )
    except FHSIS.DoesNotExist:
        fhsis = None

    records = MonthlyReweighing.objects.filter(patient__barangay=profile.barangay, date__month=datetime.now().month)

    if records.count() == 0:
        approved_mr = False
    else:
        approved_mr = records[0].status == 'Approved'


    context = {
        'profile': profile,
        'date': datetime.now(),
        'opt': opt,
        'fp': family_profiles,
        'has_mr': validations.has_monthly_reweighing(profile.barangay, datetime.now().month),
        'approved_mr': approved_mr,
        'fhsis': fhsis
    }

    return render(request, 'core/bns_index.html', context)


@login_required
def nutritionist(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'db',

    }

    return render(request, 'core/nutritionist_index.html', context)


@login_required
def mark_as_read(request, id):

    notif = Notification.objects.get(id=id)
    notif.is_read = True
    notif.save()

    previous_page = request.META['HTTP_REFERER']
    print(previous_page)

    return redirect(previous_page)


@login_required
def mark_all_as_read(request):

    notifs = Notification.objects.filter(profile_to=Profile.objects.get(user=request.user))

    for notif in notifs:
        notif.is_read = True
        notif.save()

    return redirect(request.META['HTTP_REFERER'])
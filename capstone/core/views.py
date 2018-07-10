from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from datapreprocessing.models import Metric
from friends.datainput import validations
from core.forms import UploadFileForm
from core.models import Profile, Notification
from datainput.models import OperationTimbang, MonthlyReweighing, FamilyProfile, FHSIS, NutritionalStatus, Patient
from friends import user_redirects
from datetime import datetime
from friends.datamining import correlations
from friends.datainput import misc


class SignInView(View):

    template_name = 'core/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return user_redirects.redirect_to(request.user)

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

    fhsis_current = FHSIS.objects.filter(barangay=profile.barangay, date__month=datetime.now().month,
                                               date__year=datetime.now().year)

    if fhsis_current.count() == 0:
        fhsis_date_uploaded = 'Not yet uploaded'
        fhsis_status = 'Incomplete'

    else:
        fhsis_date_uploaded = fhsis_current[0].date
        fhsis_status = 'Completed'


    has_mr = validations.has_monthly_reweighing(profile.barangay, datetime.now().month, datetime.now().year)

    if not has_mr:
        mr_uploaded = 'Not yet uploaded'
        mr_status = 'Incomplete'

    else:
        mr_uploaded = MonthlyReweighing.objects.filter(patient__barangay=profile.barangay,
                                                       date__month=datetime.now().month,
                                                       date__year=datetime.now().year).latest('date').date
        mr_status = 'Complete'

    try:
        opt = OperationTimbang.objects.get(barangay=profile.barangay, date__year=datetime.now().year)
    except OperationTimbang.DoesNotExist:
        opt = None

    if opt is None:
        opt_date = 'Not yet uploaded'
        opt_status = 'Incomplete'
    else:
        opt_date = opt.date
        opt_status = 'Completed'

    try:
        fp = FamilyProfile.objects.get(barangay=profile.barangay, date__year=datetime.now().year)
    except FamilyProfile.DoesNotExist:
        fp = None

    if fp is None:
        fp_date = 'Not yet uploaded'
        fp_status = 'Incomplete'

    else:
        fp_date = fp.date
        fp_status = 'Completed'

    request.session["active"] = 'uf';

    context2 = {
        'month_due': misc.get_due_date('monthly'),
        'profile': profile,
        'year': datetime.now().year,

        # FHSIS
        'fhsis_uploaded': fhsis_date_uploaded,
        'fhsis_status': fhsis_status,

        # reweighing
        'has_mr': has_mr,
        'mr_date': mr_uploaded,

        # OPT
        'opt_date': opt_date,
        'opt_status': opt_status,

        # family profile
        'fp_date': fp_date,
        'fp_status': fp_status,

        'active': request.session["active"]
    }

    return render(request, 'core/bns_index.html', context2)


@login_required
def nutritionist(request):
    profile = Profile.objects.get(user=request.user)

    # Nutritional Status
    nutritional_metrics = Metric.objects.filter(is_default=True, metric__contains='Nutritional Status')
    computations = [Metric.get_computations_nutritional_status(s.name) for s in NutritionalStatus.objects.all()]

    todo_list = validations.todo_list()
    print(todo_list)

    context = {
        'profile': profile,
        'active': 'db',
        'nutritional': nutritional_metrics,
        'computations_ns': computations,
        'todo_list': todo_list
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


# # # # # # # # #  DASHBOARD # # # # # # # # #
def dashboard(request):

    data = {
        'micro': Metric.get_micronutrient_dashboard(),
        'maternal': Metric.get_maternal_dashboard(),
        'child_care': Metric.get_child_care_dashboard()
    }

    return JsonResponse(data, safe=False)
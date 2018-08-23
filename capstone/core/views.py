from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from capstone.decorators import is_bns, is_nutritionist, is_program_coordinator
from causalmodel.models import Memo
from computations import weights, maternal, child_care, socioeconomic as sc
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from friends.visualizations import getters
from datapreprocessing.models import Metric
from friends.datainput import validations
from core.forms import UploadFileForm
from core.models import Profile, Notification
from datainput.models import *
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
@is_bns
def bns_index(request):

    profile = Profile.objects.get(user=request.user)

    # automatic notifications
    validations.notify_barangay(profile.barangay)

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
        'due_date_yearly': misc.get_due_date('yearly'),
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
@is_nutritionist
def nutritionist(request):

    profile = Profile.objects.get(user=request.user)

    # critical metrics dashboard by category
    criticals = Metric.critical_dashboard()

    # # Nutritional Status
    wfa = weights.get_computations_per_category('Weight for Age')
    hfa = weights.get_computations_per_category('Height for Age')
    wfhl = weights.get_computations_per_category('Weight for Height/Length')

    todo_list = validations.todo_list()

    # socioeconomic

    total = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year).count() or 1
    using_salt = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year,
                                                  is_using_iodized_salt=True).count()
    ebf = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year, is_ebf=True).count()

    socioeconomic = {
        'average_families': round(getters.get_average_family_members()),
        'is_using_salt': round(using_salt / total * 100, 2),
        'is_ebf': round(ebf / total * 100, 2)
    }

    context = {
        'profile': profile,
        'active': 'db',
        'todo_list': todo_list,

        # nutritional statuses
        'wfa': wfa['data'],
        'hfa': hfa['data'],
        'wfhl': wfhl['data'],
        'wfa_total': wfa['total'],
        'hfa_total': hfa['total'],
        'wfhl_total': wfhl['total'],

        # socioeconomic
        'average_families': socioeconomic['average_families'],

        # maternal
        # 'maternal': maternal.maternal_dashboard(1),

        # alarming metrics
        'illnesses_metrics': Metric.categorized()['illnesses'],
        'maternal_metrics': Metric.categorized()['maternal'],
        'socioeconomic_metrics': Metric.categorized()['socioeconomic'],

        'criticals': criticals
    }

    return render(request, 'core/nutritionist_index.html', context)


@login_required
@is_program_coordinator
def program_coordinator(request):
    profile = Profile.objects.get(user=request.user)

    # # Nutritional Status
    wfa = weights.get_computations_per_category('Weight for Age')
    hfa = weights.get_computations_per_category('Height for Age')
    wfhl = weights.get_computations_per_category('Weight for Height/Length')

    todo_list = validations.todo_list()

    # socioeconomic

    total = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year).count() or 1
    using_salt = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year,
                                                  is_using_iodized_salt=True).count()
    ebf = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year, is_ebf=True).count()

    socioeconomic = {
        'average_families': round(getters.get_average_family_members()),
        'is_using_salt': round(using_salt / total * 100, 2),
        'is_ebf': round(ebf / total * 100, 2)
    }

    context = {
        'profile': profile,
        'active': 'db',
        'todo_list': todo_list,

        # nutritional statuses
        'wfa': wfa['data'],
        'hfa': hfa['data'],
        'wfhl': wfhl['data'],
        'wfa_total': wfa['total'],
        'hfa_total': hfa['total'],
        'wfhl_total': wfhl['total'],

        # socioeconomic
        'average_families': socioeconomic['average_families'],

        # maternal
        # 'maternal': maternal.maternal_dashboard(1),

        # alarming metrics
        'illnesses_metrics': Metric.categorized()['illnesses'],
        'maternal_metrics': Metric.categorized()['maternal'],
        'socioeconomic_metrics': Metric.categorized()['socioeconomic'],

        'criticals': Metric.critical_dashboard()
    }

    return render(request, 'core/pc_index.html', context=context)


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

    # socioeconomic

    total = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year).count() or 1
    using_salt = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year, is_using_iodized_salt=True).count()
    ebf = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year, is_ebf=True).count()

    socioeconomic = {
        'average_families': getters.get_average_family_members(),
        'is_using_salt': round(using_salt / total * 100, 2),
        'is_ebf': round(ebf / total * 100, 2),
        'feeding': sc.get_breastfeeding()
    }

    data = {
        'micro': Metric.get_micronutrient_dashboard(),
        # 'maternal': maternal.maternal_dashboard(1),
        'child_care': Metric.get_child_care_dashboard(),
        'socioeconomic': socioeconomic
    }

    return JsonResponse(data, safe=False)


@login_required
def memos(request):

    records = Memo.objects.all()
    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    elif profile.user_type == 'Nutrition Program Coordinator':
        layout = 'core/pc_layout.html'
    else:
        layout = 'core/bns-layout.html'

    context = {
        'memos': records,
        'active': 'mm',
        'template_values': layout
    }

    return render(request, 'core/memos.html', context)


@login_required
def memo_detail(request, id):

    memo = Memo.objects.get(id=id)

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    elif profile.user_type == 'Nutrition Program Coordinator':
        layout = 'core/pc_layout.html'
    else:
        layout = 'core/bns-layout.html'

    context = {
        'active': 'mm',
        'template_values': layout,
        'memo': memo
    }

    return render(request, 'core/memo-detail.html', context)

@login_required
def memo_print(request, id):

    memo = Memo.objects.get(id=id)

    context = {
        'memo': memo
    }

    return render(request, 'core/memo-print.html', context)

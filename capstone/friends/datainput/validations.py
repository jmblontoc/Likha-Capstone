from datetime import datetime, timedelta

from configurations.models import NotifyBNS
from core.models import Notification, Profile
from datainput.models import Patient, MonthlyReweighing, HealthCareWasteManagement, InformalSettlers, UnemploymentRate, \
    FHSIS, OperationTimbang, FamilyProfile, Barangay
from friends.datainput import misc


def has_monthly_reweighing(barangay, month, year):

    patients = Patient.objects.filter(barangay=barangay)

    if patients.count() == 0:
        return False

    for patient in patients:

        try:
            mr = MonthlyReweighing.objects.get(patient=patient, date__month=month, date__year=year)
        except MonthlyReweighing.DoesNotExist:
            return False

    return True


def is_updated(patient):

    reweighs = MonthlyReweighing.objects.filter(patient=patient)

    if reweighs.count() == 0:
        return False

    for weighs in reweighs:

        if weighs.date.month == datetime.now().month and weighs.date.year == datetime.now().year:
            return True

    return False


def has_health_care():

    record = HealthCareWasteManagement.objects.filter(
        date__year=datetime.now().year
    )

    return record.count() > 0


def has_informal_settlers():

    return InformalSettlers.objects.filter(date__year=datetime.now().year, date__month=datetime.now().month).count() > 0


def has_unemployment_rate():

    return UnemploymentRate.objects.filter(date__year=datetime.now().year).count() > 0


# # # # # # # # # # # # # # # # # # # # # # # # # #

def todo_list():

    barangays = Barangay.objects.all()

    todo = []

    for b in barangays:

        if not b.has_opt:
            todo.append({
                'report_name': 'Operation Timbang',
                'barangay': b,
                'due_date': misc.get_due_date('yearly')
            })

        if not b.has_family_profile:
            todo.append({
                'report_name': 'Family Profile',
                'barangay': b,
                'due_date': misc.get_due_date('yearly')
            })

        if not b.has_reweighed:
            todo.append({
                'report_name': 'Monthly Reweighing',
                'barangay': b,
                'due_date': misc.get_due_date('monthly')
            })

        if not b.has_fhsis:
            todo.append({
                'report_name': 'FHSIS',
                'barangay': b,
                'due_date': misc.get_due_date('monthly')
            })

    return todo


def notify_barangay(barangay):

    due_list = todo_list()
    nutritionist = Profile.objects.filter(user_type__contains='Nutritionist')[0]
    notifications = Notification.objects.filter(profile_to__barangay=barangay, message__contains='Please upload')

    for data in due_list:

        if data['barangay'] == barangay:

            # check if needs to be notified
            now = datetime.now().date()

            current_notification_setting = int(NotifyBNS.objects.first().days_before)

            print(already_notified(notifications))
            if not already_notified(notifications):

                if now + timedelta(days=current_notification_setting) >= data['due_date'] or data['due_date'] <= now:

                    for bns in barangay.profile_set.all():

                        Notification.objects.create(
                            action_link='/bns',
                            profile_to=bns,
                            profile_from=nutritionist,
                            message='Please upload your %s as soon as possible' % data['report_name']
                        )


def already_notified(notifications):

    for notification in notifications:
        if notification.date.date() == datetime.now().date():
            print(notification.date.date(), datetime.now().date(), 'it goes here')
            return True

    return False

from datetime import datetime

from core.models import Notification, Profile


def get_user_type(request):

    if request.user.is_anonymous:
        return {
            'user_type': None
        }

    return {
        'user_type': Profile.objects.get(user=request.user).user_type
    }


def get_notifications(request):

    if not request.user.is_anonymous:

        notifications = Notification.objects.filter(profile_to=Profile.objects.get(user=request.user)).order_by('date')

        return {
            'notifications': notifications
        }

    return {
        'notifications': None
    }


def get_unread_notifications(request):

    if not request.user.is_anonymous:

        unread_count = Notification.objects.filter(profile_to=Profile.objects.get(user=request.user), is_read=False)

        return {
            'unread_count': unread_count.count()
        }

    return {
        'unread_count': None
    }


def today(request):

    return {
        'today': datetime.now()
    }


def year_now(request):

    return {
        'year_present': datetime.now().year
    }


def profile(request):

    if request.user.is_anonymous:
        return {
            'profile': None
        }

    return {
        'profile': Profile.objects.get(user=request.user)
    }
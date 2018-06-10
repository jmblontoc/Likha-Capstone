from core.models import Notification, Profile


def get_notifications(request):

    if not request.user.is_anonymous:

        notifications = Notification.objects.filter(profile_to=Profile.objects.get(user=request.user))

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
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
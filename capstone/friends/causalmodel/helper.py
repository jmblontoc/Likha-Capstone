from causalmodel.models import RootCause


def get_root_causes(obj):

    return [RootCause.objects.get(id=x['id']) for x in obj]


def set_root_cause(name):

    try:
        return RootCause.objects.get(name=name)
    except RootCause.DoesNotExist:
        return None
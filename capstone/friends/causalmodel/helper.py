from causalmodel.models import RootCause


def get_root_causes(obj):

    return [RootCause.objects.get(id=x['id']) for x in obj]

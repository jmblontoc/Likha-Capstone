from datainput.models import Barangay


def is_updated():

    barangays = Barangay.objects.all()

    for b in barangays:

        if not b.has_validated_reweighing or not b.has_validated_fhsis or not b.has_validated_opt or not b.has_validated_family_profiles:
            return False

    return True


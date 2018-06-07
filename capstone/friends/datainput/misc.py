

def get_fields(model):

    fields = model._meta.get_fields()

    result = []

    for field in fields:

        phrase = str(field).split('.')
        result.append(phrase[2])

    return result
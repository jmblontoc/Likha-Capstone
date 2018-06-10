from django import template
register = template.Library()

@register.filter(name='addcssclass')
def addcssclass(field):
   return field.as_widget(attrs={"class":"form-control", "placeholder":field.label})

@register.filter(name='field_type')
def field_type(field):
    return field.field.widget.__class__.__name__
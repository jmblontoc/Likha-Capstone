from django import template
register = template.Library()

@register.filter(name='addcssclass')
def addcssclass(field, css):
   return field.as_widget(attrs={"class":css})

@register.filter(name='addcssph')
def addcssph(field, css):
   return field.as_widget(attrs={"placeholder":css})
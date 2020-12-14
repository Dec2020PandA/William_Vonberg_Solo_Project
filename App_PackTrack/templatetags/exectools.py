from django import template

register = template.Library()

@register.simple_tag(name="exec")
def exec(obj, func, *args, **kwargs):
    return getattr(obj, func)(*args, **kwargs)

@register.filter(name='boolify')
def boolify(obj):
    return int(bool(obj))
# accounts/templatetags/roles_tags.py
from django import template

register = template.Library()

@register.filter
def es_jefe(user):
    return user.is_authenticated and user.groups.filter(name='Jefe').exists()

@register.filter
def es_trabajador(user):
    return user.is_authenticated and user.groups.filter(name='Trabajador').exists()

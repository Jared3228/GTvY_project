# accounts/utils.py
from django.contrib.auth.models import Group

def es_jefe(user):
    return user.is_authenticated and user.groups.filter(name='Jefe').exists()

def es_trabajador(user):
    return user.is_authenticated and user.groups.filter(name='Trabajador').exists()

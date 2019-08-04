from django import template
from django.http import request

register = template.Library()


@register.filter(name='unslug_capitalize')
def unslug_capitalize(value):
    return value.replace('-', ' ').title()


@register.filter(name='user_check')
def user_check(path, username):
    path = path.replace('/accounts/', '')
    name = path.replace('/profile/', '')
    return name == username


@register.simple_tag
def check_applications(queryset, id, user):
    for applicant in queryset:
        if applicant.user == user:
            if applicant.position.id == id:
                return applicant.status
    return 'new'

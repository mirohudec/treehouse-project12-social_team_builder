from django import template

register = template.Library()


@register.filter(name='unslug_capitalize')
def unslug_capitalize(value):
    return value.replace('-', ' ').title()

from django import template

register = template.Library()


# @register.filter(name='times')
@register.filter
def for_loop(number):
    return range(number)
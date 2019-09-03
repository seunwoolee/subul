from django import template

register = template.Library()


@register.filter
def for_loop(number):
    return range(number)

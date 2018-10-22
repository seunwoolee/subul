from django import template
register = template.Library()


@register.filter
def lookup(d, key):
    try:
        result = d[key]["amount"]
    except:
        result = 0
    return result
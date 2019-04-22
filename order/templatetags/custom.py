from django import template

register = template.Library()


@register.filter
def lookup_codeName(d, key):
    try:
        result = d[key]["codeName"]
    except:
        result = ' '
    return result


@register.filter
def lookup_specialTag(d, key):
    try:
        result = d[key]["specialTag"]
    except:
        result = ''
    return result


@register.filter
def lookup_specialTag(d, key):
    try:
        result = d[key]["specialTag"]
    except:
        result = ''
    return result


@register.filter
def lookup_totalCount(d, key):
    try:
        result = d[key]["totalCount"]
    except:
        result = ' '
    return result


@register.filter
def lookup_price(d, key):
    try:
        result = int(d[key]["pricePerEa"])
    except:
        result = ' '
    return result


@register.filter
def lookup_supplyPrice(d, key):
    try:
        result = d[key]["supplyPrice"]
    except:
        result = ' '

    if not result:
        result = ' '
    return result


@register.filter
def lookup_vatPrice(d, key):
    try:
        result = d[key]["vatPrice"]
    except:
        result = ' '

    if not result:
        result = ' '
    return result


@register.filter
def lookup_releaseVat(d, key):

    try:
        result = d[key]["releaseVat"]
    except:
        result = ' '

    if not result:
        result = ' '
    return result


@register.filter
def lookup_memo(d, key):
    try:
        result = d[key]["memo"]
    except:
        result = ' '

    if not result:
        result = ' '
    return result


@register.filter
def lookup_amount(d, key):
    try:
        result = d[key]["amount"]
    except:
        result = 0
    return result


@register.filter
def update_type(key , value):
    key = value
    return key

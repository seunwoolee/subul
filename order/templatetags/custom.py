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
def update_type(key, value):
    key = value
    return key


@register.filter
def to_yyyy_mm_dd(yyyymmdd):
    return f'{yyyymmdd[0:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:8]}'


@register.filter
def for_loop(number):
    return range(number)


@register.filter
def productOrderPacking_filter(productOrderPacking):
    return productOrderPacking.filter(type='일반')


@register.filter
def calculate_boxCount(productOrderPacking):
    real_boxCount = productOrderPacking.boxCount

    if productOrderPacking.future_stock:
        real_boxCount += productOrderPacking.future_stock.boxCount

    if productOrderPacking.past_stock:
        real_boxCount -= productOrderPacking.past_stock.boxCount

    return real_boxCount


@register.filter
def calculate_eaCount(productOrderPacking):
    real_eaCount = productOrderPacking.eaCount

    if productOrderPacking.future_stock:
        real_eaCount += productOrderPacking.future_stock.eaCount

    if productOrderPacking.past_stock:
        real_eaCount -= productOrderPacking.past_stock.eaCount

    return real_eaCount

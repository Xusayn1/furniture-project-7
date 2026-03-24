from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def get_full_path(path, code):
    split_path = path.split('/')
    split_path[1] = code
    return '/'.join(split_path)


@register.filter
def in_cart(product, request):
    cart = request.session.get('cart', [])
    return product.id in cart


@register.filter
def in_wishlist(product, request):
    wishlist = request.session.get('wishlist', [])
    return product.id in wishlist


@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    """
    Build a querystring preserving existing params and overriding with given kwargs.
    Pass value None to drop a key.
    Usage: {% querystring page=2 tag=5 %}
    """
    request = context['request']
    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            query.pop(key, None)
        else:
            query[key] = value
    qs = query.urlencode()
    return f"?{qs}" if qs else ""

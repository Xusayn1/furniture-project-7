from typing import Dict, List

from django.http import HttpRequest


CART_KEY = "cart"
WISHLIST_KEY = "wishlist"


def get_cart(session) -> Dict[str, int]:
    cart = session.get(CART_KEY, {})
    # Normalize to dict[str,int]; migrate legacy list-of-ids to qty=1
    if isinstance(cart, list):
        return {str(pid): 1 for pid in cart}
    if isinstance(cart, dict):
        return {str(k): int(v) for k, v in cart.items()}
    return {}


def save_cart(session, cart: Dict[str, int]):
    session[CART_KEY] = cart
    session.modified = True


def add_to_cart(request: HttpRequest, product_id: int, quantity: int = 1):
    cart = get_cart(request.session)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + max(quantity, 1)
    save_cart(request.session, cart)


def decrease_cart(request: HttpRequest, product_id: int, quantity: int = 1):
    cart = get_cart(request.session)
    key = str(product_id)
    if key in cart:
        cart[key] = max(cart[key] - max(quantity, 1), 0)
        if cart[key] == 0:
            cart.pop(key)
        save_cart(request.session, cart)


def remove_from_cart(request: HttpRequest, product_id: int):
    cart = get_cart(request.session)
    cart.pop(str(product_id), None)
    save_cart(request.session, cart)


def toggle_wishlist(request: HttpRequest, product_id: int):
    wishlist: List[int] = request.session.get(WISHLIST_KEY, [])
    if product_id in wishlist:
        wishlist.remove(product_id)
    else:
        wishlist.append(product_id)
    request.session[WISHLIST_KEY] = wishlist
    request.session.modified = True


def get_wishlist(session) -> List[int]:
    return session.get(WISHLIST_KEY, [])

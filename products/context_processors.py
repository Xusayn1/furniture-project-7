from decimal import Decimal

from products.models import Product


def cart_and_wishlist(request):
    """
    Inject cart / wishlist counters and cart total into templates.
    Works for anonymous users via session storage.
    """
    session = request.session
    wishlist_ids = session.get("wishlist", [])
    if not isinstance(wishlist_ids, list):
        wishlist_ids = []

    cart = session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    cart_items = []
    total_usd = Decimal("0")

    if cart:
        products = Product.objects.filter(id__in=[int(pid) for pid in cart.keys()])
        product_map = {p.id: p for p in products}
        for pid, qty in cart.items():
            product = product_map.get(int(pid))
            if not product:
                continue
            subtotal = product.price_usd * qty
            total_usd += subtotal
            cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})

    return {
        "cart_items": cart_items,
        "cart_count": sum(cart.values()),
        "cart_total_usd": total_usd,
        "wishlist_count": len(wishlist_ids),
    }

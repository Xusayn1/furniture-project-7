from decimal import Decimal

from products.models import Product


def cart_and_wishlist(request):
    """
    Inject cart / wishlist counters and cart total into templates.
    Works for anonymous users via session storage.
    """
    session = request.session
    wishlist_ids = session.get("wishlist", [])
    cart = session.get("cart", {})

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
        "cart_count": sum(cart.values()) if isinstance(cart, dict) else 0,
        "cart_total_usd": total_usd,
        "wishlist_count": len(wishlist_ids) if isinstance(wishlist_ids, list) else 0,
    }

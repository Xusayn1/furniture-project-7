from decimal import Decimal

from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView

from products.models import Product, ProductCategory, ProductTag, ProductColor, Manufacture


class ProductListView(ListView):
    model = Product
    template_name = 'products/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        manufacture = self.request.GET.get('manufacture')
        tag = self.request.GET.get('tag')
        color = self.request.GET.get('color')
        q = self.request.GET.get('q')
        ordering = self.request.GET.get('ordering')
        if q:
            queryset = queryset.filter(Q(name__icontains=q))

        if manufacture:
            queryset = queryset.filter(manufacture__id=int(manufacture))
        if tag:
            queryset = queryset.filter(tags__id=int(tag))
        if color:
            queryset = queryset.filter(colors__id=int(color))

        if ordering in ['name', '-name', 'price_uzs', '-price_uzs']:
            queryset = queryset.order_by(ordering)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['tags'] = ProductTag.objects.all()
        context['colors'] = ProductColor.objects.all()
        context['manufactures'] = Manufacture.objects.filter(is_active=True)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


def add_or_remove_from_cart(request, pk):
    """
    Add, remove or adjust quantities in the session cart.
    Cart is stored as {product_id: qty}.
    """
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    product_key = str(pk)
    action = request.GET.get('action', 'toggle')
    try:
        qty = max(int(request.GET.get('qty', 1)), 1)
    except (TypeError, ValueError):
        qty = 1

    if action == 'add':
        cart[product_key] = cart.get(product_key, 0) + qty
    elif action == 'decrease':
        if product_key in cart:
            new_qty = cart[product_key] - qty
            if new_qty > 0:
                cart[product_key] = new_qty
            else:
                cart.pop(product_key, None)
    elif action == 'remove':
        cart.pop(product_key, None)
    else:  # toggle behaviour
        if product_key in cart:
            cart.pop(product_key, None)
        else:
            cart[product_key] = qty

    request.session['cart'] = cart
    request.session.modified = True
    next_url = request.GET.get('next', reverse_lazy('products:list'))
    return redirect(next_url)


def add_or_remove_from_wishlist(request, pk):
    wishlist = request.session.get('wishlist', [])
    # session = {
    #     'cart': {
    #         1: {
    #             "quantity": 2,
    #             "color": 1
    #         }
    #     }
    # }
    if pk in wishlist:
        wishlist.remove(pk)
    else:
        wishlist.append(pk)

    request.session['wishlist'] = wishlist
    next_url = request.GET.get('next', reverse_lazy('products:list'))
    return redirect(next_url)


class WishlistListView(ListView):
    template_name = 'products/wishlist.html'
    paginate_by = 2
    context_object_name = 'products'

    def get_queryset(self):
        wishlist = self.request.session.get('wishlist', [])
        return Product.objects.filter(id__in=wishlist, is_active=True)


class CartListView(TemplateView):
    template_name = 'products/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        if not isinstance(cart, dict):
            cart = {}

        product_ids = [int(pid) for pid in cart.keys()]
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        product_map = {str(p.id): p for p in products}

        items = []
        total = Decimal('0')
        for pid, qty in cart.items():
            product = product_map.get(str(pid))
            if not product:
                continue
            subtotal = product.price_usd * qty
            total += subtotal
            items.append({'product': product, 'qty': qty, 'subtotal': subtotal})

        context.update({'items': items, 'total': total})
        return context

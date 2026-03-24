from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from products.models import Product, ProductCategory, ProductTag, ProductColor, Manufacture
from products.utils import (
    add_to_cart,
    decrease_cart,
    remove_from_cart,
    toggle_wishlist,
    get_cart,
    get_wishlist,
)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).prefetch_related('images')

        manufacture = self.request.GET.get('manufacture')
        tag = self.request.GET.get('tag')
        color = self.request.GET.get('color')
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        if manufacture:
            queryset = queryset.filter(manufacture__id=int(manufacture))
        if tag:
            queryset = queryset.filter(tags__id=int(tag))
        if color:
            queryset = queryset.filter(colors__id=int(color))
        if category:
            queryset = queryset.filter(categories__id=int(category))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['tags'] = ProductTag.objects.all()
        context['colors'] = ProductColor.objects.all()
        context['manufactures'] = Manufacture.objects.filter(is_active=True)
        context['current_filters'] = {
            "manufacture": self.request.GET.get('manufacture'),
            "tag": self.request.GET.get('tag'),
            "color": self.request.GET.get('color'),
            "category": self.request.GET.get('category'),
            "q": self.request.GET.get('q', ''),
        }
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related('images')


def add_or_remove_from_cart(request, pk):
    action = request.GET.get('action', 'add')
    try:
        qty = int(request.GET.get('qty', 1))
    except (TypeError, ValueError):
        qty = 1
    qty = max(qty, 1)

    if action == 'remove':
        remove_from_cart(request, pk)
    elif action == 'decrease':
        decrease_cart(request, pk, qty)
    else:
        add_to_cart(request, pk, qty)

    next_url = request.GET.get('next', reverse_lazy('products:list'))
    return redirect(next_url)


def add_or_remove_from_wishlist(request, pk):
    """
    Toggle the product in the user's wishlist stored in the session.
    If the product is already present it will be removed, otherwise added.
    """
    toggle_wishlist(request, pk)
    next_url = request.GET.get('next', reverse_lazy('products:list'))
    return redirect(next_url)


def wishlist_view(request):
    """Show products saved in the session wishlist."""
    wishlist_ids = get_wishlist(request.session)
    products = Product.objects.filter(id__in=wishlist_ids, is_active=True).prefetch_related('images')
    return render(request, 'products/wishlist.html', {'products': products})


def cart_view(request):
    """Display cart contents with quantities from session."""
    cart = get_cart(request.session)
    products = Product.objects.filter(id__in=[int(pid) for pid in cart.keys()], is_active=True).prefetch_related('images')
    product_map = {str(p.id): p for p in products}
    items = []
    total = 0
    for pid, qty in cart.items():
        product = product_map.get(str(pid))
        if not product:
            continue
        subtotal = product.price_usd * qty
        total += subtotal
        items.append({"product": product, "qty": qty, "subtotal": subtotal})

    return render(
        request,
        'products/cart.html',
        {
            "items": items,
            "total": total,
        },
    )

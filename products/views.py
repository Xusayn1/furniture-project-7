from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

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
    cart = request.session.get('cart', [])
    # session = {
    #     'cart': {
    #         1: {
    #             "quantity": 2,
    #             "color": 1
    #         }
    #     }
    # }
    if pk in cart:
        cart.remove(pk)
    else:
        cart.append(pk)

    request.session['cart'] = cart
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


class CartListView(ListView):
    template_name = 'products/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        cart = self.request.session.get('cart', [])
        return Product.objects.filter(id__in=cart, is_active=True)
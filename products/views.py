from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product, ProductCategory, ProductTag, ProductColor, Manufacture




class ProductListlView(ListView):
    model = Product
    template_name = 'products/products-list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)

        manufacture = self.request.GET.get('manufacture')
        tag = self.request.GET.get('tag')
        color = self.request.GET.get('color')

        if manufacture:
            queryset = queryset.filter(manufacture__id=int(manufacture))

        if tag:
            queryset = queryset.filter(tags__id=int(tag))

        if color:
            queryset = queryset.filter(colors__id=int(color))

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['tags'] = ProductTag.objects.all()
        context['colors'] = ProductColor.objects.all()
        context['manufactures'] = Manufacture.objects.filter(is_active=True)
        return context
    
class ProductDetailView(ListView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(id=self.kwargs['pk'], is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_queryset().first()
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['tags'] = ProductTag.objects.all()
        context['colors'] = ProductColor.objects.all()
        context['manufactures'] = Manufacture.objects.filter(is_active=True)
        context['related_products'] = Product.objects.filter(categories__in=product.categories.values_list('id', flat=True)).exclude(
            id=product.id).distinct()[:4]
        return context
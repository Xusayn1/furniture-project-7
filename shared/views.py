from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, TemplateView
from shared.forms import ContactForm
from shared.models import Team
from products.models import Product


class HomePageView(TemplateView):
    template_name = 'shared/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_products'] = Product.objects.filter(is_active=True).prefetch_related('images')[:8]
        return context
    



    
class ContactPageView(FormView):
    template_name = 'shared/contact.html'
    context_object_name = 'form'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        text = _("Successfully sent to the admin, thanks for your attention.")
        messages.success(self.request, text)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field}: {error}")

        error_text = " | ".join(errors)
        messages.error(self.request, error_text)
        return super().form_invalid(form)
    




class AboutPageView(ListView):
    model = Team
    template_name = 'shared/about-us.html'
    context_object_name = 'members'
    queryset = Team.objects.filter(is_active=True).order_by("-created_at")

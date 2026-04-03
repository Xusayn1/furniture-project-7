from django.shortcuts import render


def handler404(request, exception, template_name="shared/404.html"):
    return render(request, template_name, status=404)


def handler500(request, template_name="shared/500.html"):
    return render(request, template_name, status=500)


def handler403(request, exception, template_name="shared/403.html"):
    return render(request, template_name, status=403)

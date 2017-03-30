"""Application views."""

import django.views.generic


class IndexView(django.views.generic.TemplateView):
    """Render 'index.html' template."""

    template_name = 'index.html'
    http_method_names = (u'get', )


class LeageView(django.views.generic.TemplateView):
    """Render 'about.html' template."""

    template_name = 'leages.html'
    http_method_names = (u'get', )
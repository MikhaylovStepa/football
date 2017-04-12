import django.template


def multiply(initial):
    return initial + 1


register = django.template.Library()
register.simple_tag(multiply)
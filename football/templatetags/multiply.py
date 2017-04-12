import django.template

class yrange:
    def __init__(self):
        self.i=0

    def __iter__(self):
        return self

    def next(self):
        i = self.i
        self.i = self.i+1
        return i

def multiply(initial, value, arg):
    initial = yrange()
    return initial.next()


register = django.template.Library()
register.simple_tag(multiply)
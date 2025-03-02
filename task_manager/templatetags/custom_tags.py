from django import template

register = template.Library()


@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    return None


@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})

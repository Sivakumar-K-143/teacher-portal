from django import template

register = template.Library()

@register.filter
def initials(name):
    if not name:
        return ''
    return ''.join([part[0] for part in name.split() if part]).upper()

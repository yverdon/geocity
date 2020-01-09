from django import template

register = template.Library()

@register.inclusion_tag('permits/_permit_progressbar.html')
def permit_progressbar(format_string):
    return 'toto'

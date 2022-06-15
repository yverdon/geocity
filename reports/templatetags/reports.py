from django import template

register = template.Library()


@register.simple_tag
def render_section(obj, **context):
    return obj.render(context)

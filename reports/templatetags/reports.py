from django import template

register = template.Library()


@register.simple_tag
def render(template_str, data):
    # TODO CRITICAL: rendering user data is NOT SAFE, we should use sandboxed jinja instead (or other safe alternative)
    return template.Template(template_str).render(template.Context({"data": data}))

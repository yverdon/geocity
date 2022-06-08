import typing
from django import template
from django.utils.safestring import mark_safe
from jinja2.sandbox import SandboxedEnvironment

register = template.Library()


@register.simple_tag
def render_user_template(template_str, data):
    """Renders a user given template in a hopefully safe way"""
    env = SandboxedEnvironment()
    contents = env.from_string(template_str).render({"data": data})
    return mark_safe(contents)


@register.filter
def iterate_nested_dict(data):
    """Iterate recursively through a dict, returning keys, value and class in a flat list."""

    def _iterate(val, keys: list):
        if isinstance(val, dict):
            for k, v in val.items():
                yield from _iterate(v, [*keys, str(k)])
        else:
            yield (".".join(keys), repr(val), val.__class__.__name__)

    return _iterate(data, ["data"])

import typing
from django import template

register = template.Library()


@register.simple_tag
def render(template_str, data):
    # TODO CRITICAL: rendering user data is NOT SAFE, we should use sandboxed jinja instead (or other safe alternative)
    return template.Template(template_str).render(template.Context({"data": data}))


@register.filter
def iterate_nested_dict(data):
    """Iterate recursively through a dict, returning keys, value and class in a flat list."""

    def _iterate(val, keys: list):
        if isinstance(val, dict):
            for k,v in val.items():
                yield from _iterate(v, [*keys, str(k)])
        else:
            yield (".".join(keys), repr(val), val.__class__.__name__)

    return _iterate(data, ["data"])

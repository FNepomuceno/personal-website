from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.staticfiles import finders

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])


@register.filter()
@stringfilter
def print_static(value):
    try:
        filepath = finders.find(value)
        if not filepath:
            filepath = ''
        with open(filepath) as file:
            return file.read()
    except FileNotFoundError:
        return '#FILE NOT FOUND'

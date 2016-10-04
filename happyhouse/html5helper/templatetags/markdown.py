# coding=utf-8

from django.utils.safestring import mark_safe
from django import template

from html5helper.utils import make_markdown

register = template.Library()


@register.filter("markdown")
def do_markdown(text):
    if not text:
        return ""
    return mark_safe(make_markdown(text))

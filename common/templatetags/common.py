'''Collection of common templatetags'''
from typing import Dict

from urlobject import URLObject

from django import template
from django.urls import translate_url
from django.forms import ModelForm
from django.template import RequestContext
from django.core.paginator import Page

import common.types as types

register = template.Library()


@register.simple_tag(takes_context=True)
def change_lang(context: RequestContext, lang: str, *args, **kwargs) -> str:
    '''Change website language'''
    path = context["request"].path
    return translate_url(path, lang)


@register.inclusion_tag('templatetags/filter_form_block.html')
def filter_form_block(form: ModelForm) -> types.CustomFormType:
    '''Filter form template tag'''
    return {'form': form}


@register.inclusion_tag('templatetags/filter_form_block_vessel.html')
def filter_form_block_vessel(form: ModelForm) -> types.CustomFormType:
    '''Filter form template tag'''
    return {'form': form}


@register.inclusion_tag('templatetags/boolean_icon.html')
def boolean_icon(condition: bool) -> types.CustomConditionType:
    '''Boolean field tempalte tag'''
    return {'condition': condition}


@register.inclusion_tag('templatetags/pagination.html')
def pagination(page_obj: Page) -> types.CustomPageType:
    '''Pagination template tag'''
    return {'page_obj': page_obj}


@register.inclusion_tag('templatetags/head_cell_with_ordering.html', takes_context=True)
def head_cell_with_ordering(
    context: RequestContext, field: str, title: str) -> types.CustomHeadCellType:
    '''Header cell with ordering template tag'''
    desc_field = f'-{field}'
    current_order_by = context['order_by']
    order_by = desc_field if current_order_by == field else field
    arrow_class = None
    if current_order_by == desc_field:
        arrow_class = 'up'
    if current_order_by == field:
        arrow_class = 'down'

    return {
        'title': title,
        'field': field,
        'arrow_class': arrow_class,
        'ordering_fields': context['ordering_fields'],
        'order_by': order_by
    }


@register.simple_tag(takes_context=True)
def change_url(context: RequestContext, **kwargs) -> str:
    '''Change url template tag'''
    url = URLObject(context.request.get_full_path())
    path = url.path
    query = url.query
    for k, v in kwargs.items():
        query = query.set_param(k, v)
    return f'{path}?{query}'

from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def get_url(model_name, action):

    model = ContentType.objects.get(model=model_name.lower())
    app_name = model.model_class()._meta.app_label
    urls_dict = f'{ model_name.lower() }_urls'
    urls = getattr(__import__(f'{ app_name }.configs', fromlist=[urls_dict]), urls_dict)
    url = urls.get(action, None)

    return url if url is not None else ''

@register.simple_tag
def get_order(order):

    if '-' in order:
        new_order = order.split('-')[1]
    else:
        new_order = f'-{ order }'

    return new_order


@register.simple_tag
def get_breadcrumbs(url):

    return url.split('/')
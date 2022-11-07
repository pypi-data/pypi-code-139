
from django.core.management.base import BaseCommand
from django.conf import settings

from dashboard.generators import AbstractGenerator


class Command(BaseCommand):
    """
    """

    help = 'Generate'

    def add_arguments(self, parser):

        parser.add_argument('app_name', type=str, help='App name to generate.')

        parser.add_argument('--urls', action='store_true', help='Only generate urls')
        parser.add_argument('--forms', action='store_true', help='Only generate forms')
        parser.add_argument('--filters', action='store_true', help='Only generate filters')
        parser.add_argument('--views', action='store_true', help='Only generate views')

    def handle(self, *args, **kwargs):

        app_name = kwargs['app_name']
        app_module = None

        urls = kwargs['urls']
        forms = kwargs['forms']
        filters = kwargs['filters']
        views = kwargs['views']

        all = not urls and not forms and not filters and not views
        
        for app in settings.CUSTOM_INSTALLED_APPS:
            if app == app_name:
                app_module = True
                break
        
        if not app_module:
            raise Exception(f'App name "{ app_name }" not installed.')
        
        generator = AbstractGenerator(app)

        # Urls
        if all or urls:
            generator.generate_urls()

        # Forms
        if all or forms:
            generator.generate_forms()

        # Filters
        if all or filters:
            generator.generate_filters()

        # Views
        if all or views:
            generator.generate_views()

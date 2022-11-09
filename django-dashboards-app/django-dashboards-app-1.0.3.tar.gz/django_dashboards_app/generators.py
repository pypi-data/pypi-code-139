
import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


class AbstractGenerator:

    actions = ['List', 'Filter', 'Create', 'Detail', 'Update', 'Delete']

    def __init__(self, app, *args, **kwargs) -> None:
        
        self.app = app
        self.models = [x.model_class() for x in ContentType.objects.filter(app_label=app)]
    
    def generate_urls(self):
        
        lines = []

        lines.append('from django.urls import path')
        lines.append('from django.views.generic import RedirectView')
        lines.append('')
        lines.append(f'from { self.app } import base_views\n\n')
        lines.append('urlpatterns = [')
        lines.append('')
        lines.append(f"    path('', RedirectView.as_view(url='{ self.models[0].__name__.lower() }/'), name='home'),")

        for model in self.models:

            model_name = model.__name__
            model_name_lower = model_name.lower()

            lines.append("    ")
            lines.append(f"    # { model_name }")
            lines.append(f"    path('{ model_name_lower }/', base_views.Base{ model_name }ListView.as_view(), name='{ model_name_lower }_list'),")
            lines.append(f"    path('{ model_name_lower }/create/', base_views.Base{ model_name }CreateView.as_view(), name='{ model_name_lower }_create'),")
            lines.append(f"    path('{ model_name_lower }/filter/', base_views.Base{ model_name }FilterView.as_view(), name='{ model_name_lower }_filter'),")
            lines.append(f"    path('{ model_name_lower }/<pk>/detail/', base_views.Base{ model_name }DetailView.as_view(), name='{ model_name_lower }_detail'),")
            lines.append(f"    path('{ model_name_lower }/<pk>/update/', base_views.Base{ model_name }UpdateView.as_view(), name='{ model_name_lower }_update'),")
            lines.append(f"    path('{ model_name_lower }/<pk>/delete/', base_views.Base{ model_name }DeleteView.as_view(), name='{ model_name_lower }_delete'),")
        
        lines.append(']')

        file = open(f'{ settings.BASE_DIR }/{ self.app }/base_urls.py', 'w')

        for line in lines:
            file.write(f'{line}\n')

        file.close()
    
    def generate_forms(self):
        
        lines = []

        lines.append('from django_dashboards_app.forms import AbstractModelForm')
        lines.append(f'from { self.app } import models')

        for model in self.models:

            model_name = model.__name__
            model_name_lower = model_name.lower()

            lines.append('\n')
            lines.append(f"class Base{ model_name }Form(AbstractModelForm):")
            lines.append("    class Meta:")
            lines.append(f"        model = models.{ model_name }")
            lines.append("        fields = '__all__'")
        
        lines.append('\n')

        file = open(f'{ settings.BASE_DIR }/{ self.app }/base_forms.py', 'w')

        for line in lines:
            file.write(f'{line}\n')

        file.close()
    
    def generate_filters(self):
        
        lines = []

        lines.append('from django_dashboards_app.filters import AbstractModelFilter')
        lines.append(f'from { self.app } import models')

        for model in self.models:

            model_name = model.__name__
            model_name_lower = model_name.lower()

            lines.append('\n')
            lines.append(f"class Base{ model_name }Filter(AbstractModelFilter):")
            lines.append("    class Meta:")
            lines.append(f"        model = models.{ model_name }")
            lines.append("        fields = '__all__'")
        
        lines.append('\n')

        file = open(f'{ settings.BASE_DIR }/{ self.app }/base_filters.py', 'w')

        for line in lines:
            file.write(f'{line}\n')

        file.close()
    
    def generate_views(self):
        
        lines = []

        lines.append('from django_dashboards_app import views as abstract_views')
        lines.append(f'from { self.app } import models')

        for model in self.models:

            model_name = model.__name__
            model_name_lower = model_name.lower()

            lines.append('\n')

            lines.append(f"# { model_name }")

            for action in self.actions:
                
                lines.append(f"class Base{ model_name }{ action }View(abstract_views.Abstract{ action }View):")
                lines.append(f"    model = models.{ model_name }")
        
        lines.append('\n')

        file = open(f'{ settings.BASE_DIR }/{ self.app }/base_views.py', 'w')

        for line in lines:
            file.write(f'{line}\n')

        file.close()
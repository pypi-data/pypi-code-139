
from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django_filters.views import FilterView

from django_dashboards_app.forms import AbstractConfirmationForm


# Create your views here.
def apps(request):

    apps = settings.CUSTOM_INSTALLED_APPS

    return render(request, 'apps.html', {
        'apps': apps
    })


class AbstractBaseView(View):

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        if hasattr(self, 'model') and self.model is not None:
            self.model = self.model
        elif hasattr(self, 'queryset') and self.queryset is not None:
            self.model = self.queryset.model
        else:
            raise Exception('Model or Queryset will be prvided.')

        self.app_name = self.model._meta.app_label
        self.model_name = self.model.__name__
        self.model_name_verbose = self.model._meta.verbose_name
        self.model_name_verbose_plural = self.model._meta.verbose_name_plural

        self.get_navbar()
    
    def get_navbar(self):
        
        self.navbar = list(
            map(
                lambda x: {
                    'name': x.model_class()._meta.verbose_name.lower(),
                    'verbose_name': x.model_class()._meta.verbose_name
                },
                ContentType.objects.filter(app_label=self.app_name)
            )
        )

    def get_form_class_name(self):

        return f'Base{ self.model_name }Form'
    
    def get_form_class(self):

        form_class_name = self.get_form_class_name()
        
        return getattr(__import__(f'{ self.app_name }.base_forms', fromlist=[form_class_name]), form_class_name)
    
    def get_template_form_name(self):

        template_form_name = None

        for template in [f'{ self.model_name.lower() }_{ self.action }_form.html', f'{ self.model_name.lower() }_form.html', 'form.html']:
            
            try:
                exist = get_template(template)
            except Exception as e:
                exist = None

            if exist:
                template_form_name = template
                break
        
        return template_form_name

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context.update({
            'settings': settings,
            'app_name': self.app_name,
            'model': self.model,
            'model_name': self.model_name,
            'model_name_verbose': self.model_name_verbose,
            'model_name_verbose_plural': self.model_name_verbose_plural,
            'navbar': self.navbar
        })
        
        return context
        

class AbstractListView(PermissionRequiredMixin, FilterView, AbstractBaseView, ListView):
    
    action = 'list'

    # Templates
    template_name = None
    template_preview_name = None
    template_actions_name = None

    # Ordering
    order = None

    # Pagination
    paginate_by = None
    page = None

    # Filters
    filterset_class = None
    filters = None
    template_filters = None


    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        # Pagination
        if not self.paginate_by:
            self.paginate_by = 1

        # Filters
        if not self.filterset_class:
            filter_class_name = f'Base{ self.model_name }Filter'
            self.filterset_class = getattr(__import__(f'{ self.app_name }.base_filters', fromlist=[filter_class_name]), filter_class_name)
        
        # Templates
        if not self.template_name:
            self.template_name = 'list.html'

        if not self.template_preview_name:
            self.template_preview_name = self.get_template_preview_name()
        
        if not self.template_actions_name:
            self.template_actions_name = self.get_template_actions_name()

        # Permissions
        self.permission_required = (self.model_name.lower() + '.can_view')

    def get_template_preview_name(self):

        template_preview_name = None

        for template in [f'{ self.model_name.lower() }_preview.html', 'preview.html']:
            
            try:
                exist = get_template(template)
            except Exception as e:
                exist = None

            if exist:
                template_preview_name = template
                break
        
        return template_preview_name
    
    def get_template_actions_name(self):

        template_actions_name = None

        for template in [f'{ self.model_name.lower() }_actions.html', 'actions.html']:
            
            try:
                exist = get_template(template)
            except Exception as e:
                exist = None

            if exist:
                template_actions_name = template
                break
        
        return template_actions_name

    def get(self, request, *args, **kwargs):

        self.request_data = request.GET.copy()

        self.get_ordering()
        self.get_pagination()
        self.get_filters()

        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        queryset = self.filterset_class(
            self.request.GET,
            self.model.objects.all().order_by(self.order)
        ).qs

        return queryset

    def get_ordering(self):

        # from model
        try:
            model_order = self.model._meta.ordering[0]
        except Exception:
            model_order = None

        # from request
        try:
            request_order = self.request_data.pop('order', None)[0]
        except Exception:
            request_order = None
        
        if request_order:
            self.order = request_order
        elif model_order:
            self.order = model_order
        else:
            self.order = self.model._meta.pk.name

        self.model_fields = list(map(lambda x: { 'name': x.name, 'verbose_name': x.verbose_name }, self.model._meta.fields))
    
    def get_pagination(self):

        self.page = self.request_data.pop('page', 1)
        self.paginate_by = self.request_data.pop('paginate_by', [self.paginate_by])[0]

    def get_filters(self):

        filters = {}
        template_filters = {}

        for key, value in self.request_data.items():
            filters[key] = value

            try:
                attr = getattr(self.model, key).field
                attr_class_name = attr.__class__.__name__
                attr_verbose_name = attr.verbose_name

            except Exception as e:
                attr = None
                attr_class_name = ''
                submodel_class = getattr(__import__(f'{ self.app_name }.models', fromlist=[key.capitalize()]), key.capitalize())
                attr_verbose_name = submodel_class._meta.verbose_name
                value = submodel_class.objects.get(id=value)

            template_filters[key] = { 'verbose': attr_verbose_name }

            if attr_class_name == 'BooleanField':
                template_filters[key]['value'] = value

            elif attr_class_name == 'ForeignKey':
                subelement_class = getattr(__import__(f'{ self.app_name }.models', fromlist=[key.capitalize()]), key.capitalize())
                template_filters[key]['value'] = subelement_class.objects.get(id=value).__str__()

            else:
                template_filters[key]['value'] = value

        self.filters = ''.join([f'&{key}={value}' for key, value in filters.items() if value is not None and value != ''])
        self.template_filters = template_filters


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update({
            'action': self.action,
            'order': self.order,
            'filters': self.filters,
            'template_filters': self.template_filters,
            'template_preview_name': self.template_preview_name,
            'template_actions_name': self.template_actions_name,
            'model_fields': self.model_fields
        })

        return context


class AbstractFilterView(PermissionRequiredMixin, AbstractBaseView, FormView):

    action = 'filter'

    # Templates
    template_name = None
    template_form_name = None

    # Forms
    form_class = None

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        self.permission_required = (self.model_name.lower() + '.can_filter')

        # Templates
        if not self.template_name:
            self.template_name = 'filter.html'
        
        if not self.template_form_name:
            self.template_form_name = self.get_template_form_name()

        # Forms
        if not self.form_class:
            self.form_class = self.get_form_class()

    def get_success_url(self):

        url = reverse(f'{ self.app_name }:{ self.model_name.lower() }_list')
        query_params = '&'.join([f'{key}={value}' for key, value in self.request_data.items() if value is not None and value != '' and key != 'csrfmiddlewaretoken'])
        url = '?'.join((url, query_params))
        
        return url

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs['action'] = self.action
        kwargs['app_name'] = self.app_name

        return kwargs

    def post(self, request, *args, **kwargs):

        self.request_data = request.POST.copy()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        context.update({
            'action': self.action
        })
        
        return context


class AbstractCreateView(PermissionRequiredMixin, AbstractBaseView, CreateView):

    action = 'create'

    # Templates
    template_name = None
    template_form_name = None

    # Forms
    form_class = None

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        self.permission_required = (self.model_name.lower() + '.can_add')

        # Forms
        if not self.form_class:
            self.form_class = self.get_form_class()

        # Templates
        if not self.template_name:
            self.template_name = 'create.html'

        if not self.template_form_name:
            self.template_form_name = self.get_template_form_name()

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs['action'] = self.action
        kwargs['app_name'] = self.app_name

        return kwargs
    
    def get_success_url(self):

        return reverse(f'{ self.app_name }:{ self.model_name.lower() }_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context.update({
            'template_form_name': self.template_form_name,
            'action': self.action
        })

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object._req = self.request

        if hasattr(self.model, 'user') and self.request.user:
            self.object.user_id = self.request.user.id

        self.object.save()

        messages.success(self.request, f'{str(self.model_name_verbose)} creado correctamente.')

        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        
        messages.error(self.request, 'El formulario contiene errores.')

        return self.render_to_response(self.get_context_data(form=form))


class AbstractDetailView(PermissionRequiredMixin, AbstractBaseView, DetailView, UpdateView):

    action = 'detail'

    # Templates
    template_name = None
    template_form_name = None

    # Forms
    form_class = None

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        self.permission_required = (self.model_name.lower() + '.can_view')

        # Forms
        if not self.form_class:
            self.form_class = self.get_form_class()

        # Templates
        if not self.template_name:
            self.template_name = 'detail.html'

        if not self.template_form_name:
            self.template_form_name = self.get_template_form_name()

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs['action'] = self.action
        kwargs['app_name'] = self.app_name

        return kwargs

    def get_success_url(self):

        return reverse(f'{ self.app_name }:{ self.model_name.lower() }_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context.update({
            'template_form_name': self.template_form_name,
            'action': self.action,
        })
        
        return context


class AbstractUpdateView(PermissionRequiredMixin, AbstractBaseView, UpdateView):

    action = 'update'

    # Templates
    template_name = None
    template_form_name = None

    # Forms
    form_class = None

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        self.permission_required = (self.model_name.lower() + '.can_change')

        # Forms
        if not self.form_class:
            self.form_class = self.get_form_class()

        # Templates
        if not self.template_name:
            self.template_name = 'update.html'
            
        if not self.template_form_name:
            self.template_form_name = self.get_template_form_name()

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs['action'] = self.action
        kwargs['app_name'] = self.app_name

        return kwargs

    def get_success_url(self):

        return reverse(f'{ self.app_name }:{ self.model_name.lower() }_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update({
            'template_form_name': self.template_form_name,
            'action': self.action,
        })

        return context
    
    def form_valid(self, form):

        self.object = form.save()

        messages.success(self.request, f'{str(self.model_name_verbose)} actualizado correctamente.')

        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        
        messages.error(self.request, 'El formulario contiene errores.')

        return self.render_to_response(self.get_context_data(form=form))


class AbstractDeleteView(PermissionRequiredMixin, AbstractBaseView, DeleteView):

    action = 'delete'

    # Templates
    template_name = None
    template_form_name = None

    # Forms
    form_class = AbstractConfirmationForm

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        self.permission_required = (self.model_name.lower() + '.can_delete')
    
        # Forms
        if not self.form_class:
            self.form_class = self.get_form_class()

        # Templates
        if not self.template_name:
            self.template_name = 'delete.html'

        if not self.template_form_name:
            self.template_form_name = self.get_template_form_name()
    

    def get_form_class(self):

        return self.form_class

    def get_success_url(self):

        return reverse(f'{ self.app_name }:{self.model_name.lower()}_list')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        print(context)
        context.update({
            'template_form_name': self.template_form_name,
            'action': self.action
        })
        print(context)
        
        return context

    def form_valid(self, form):

        self.object._req = self.request

        messages.success(self.request, f'{str(self.model_name_verbose)} borrado correctamente.')

        return super().form_valid(form)
    
    def form_invalid(self, form):
        
        messages.error(self.request, 'El formulario contiene errores.')

        return self.render_to_response(self.get_context_data(form=form))


class AbstractExportView(PermissionRequiredMixin, AbstractBaseView, ListView):

    action = 'export'

    def setup(self, request, *args, **kwargs):

        super().setup(request, *args, **kwargs)

        self.permission_required = (self.model_name.lower() + '.can_export')

        export_class_name = self.model_name + 'Resource'
        self.export_class = getattr(__import__(f'{ self.app_name }.resources', fromlist=[export_class_name]), export_class_name)

    def get(self, request, *args, **kwargs):

        data = self.export_class().export(self.queryset)

        file_time = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
        file_name = f'{self.model_name_plural}_{file_time}.csv'

        response = HttpResponse(data.csv, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return response
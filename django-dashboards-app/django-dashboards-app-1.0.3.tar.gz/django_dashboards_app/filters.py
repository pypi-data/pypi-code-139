
from datetime import datetime

from django.db import models

import django_filters as filters


# Create your filters here.
class AbstractModelFilter(filters.FilterSet):

    class Meta:
        filter_overrides = {
             models.ImageField: {
                 'filter_class': filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
        }

    def filter_by_range_number(self, queryset, name, value):

        dates = value.split('-')

        params = {
            name + '__lte': dates[1].strip(),
            name + '__gte': dates[0].strip()
        }

        return queryset.filter(**params)

    def filter_by_range_date(self, queryset, name, value):

        dates = value.split('-')

        params = {
            name + '__lte': datetime.strptime(dates[1].strip(), '%d/%m/%Y'),
            name + '__gte': datetime.strptime(dates[0].strip(), '%d/%m/%Y')
        }

        return queryset.filter(**params)
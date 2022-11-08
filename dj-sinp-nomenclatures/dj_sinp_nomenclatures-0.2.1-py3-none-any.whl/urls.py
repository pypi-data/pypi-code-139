from django.urls import path

from .views import (
    NomenclatureViewset,
    SourceViewset,
    TypeViewset,
)
from django.urls import path, include

from rest_framework import routers

router = routers.SimpleRouter()
app_name = "sinp_nomenclatures"

router = DefaultRouter()

router.register(r'sources', SourceViewset,'sources')
router.register(r'types', TypeViewset, 'types')
router.register(r'nomenclatures', NomenclatureViewset, 'nomenclaturess')

urlpatterns = [
    path('', include(router.urls))
]

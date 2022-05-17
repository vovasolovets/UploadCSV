from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import viewsets

router = DefaultRouter(trailing_slash=False)
router.register('datasets', viewsets.DataSetViewSet, basename='datasets')
examples_router = NestedDefaultRouter(router, r'datasets', lookup='data_set')
examples_router.register(r'examples', viewsets.DataSetExampleViewSet, basename='examples')
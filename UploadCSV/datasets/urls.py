from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter(trailing_slash=False)
router.register('datasets', viewsets.DataSetViewSet, basename='datasets')
router.register('examples', viewsets.DataSetExampleViewSet, basename='examples')
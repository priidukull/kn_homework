from django.urls import include, path
from rest_framework import routers

from kn_homework.shipments_api import views

router = routers.DefaultRouter()
router.register(r'shipments', views.ShipmentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
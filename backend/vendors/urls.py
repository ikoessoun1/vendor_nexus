from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, ServiceViewSet, ContactViewSet, ContractViewSet, DocumentViewSet, VendorDetailView

router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),

]

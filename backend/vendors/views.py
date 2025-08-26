from rest_framework import viewsets, filters, permissions, generics
from .models import Vendor, Service, Contact, Contract, Document
from .serializers import VendorSerializer, ServiceSerializer, ContactSerializer, ContractSerializer, DocumentSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import PermissionDenied


# class VendorViewSet(viewsets.ModelViewSet):

        #     queryset = Vendor.objects.prefetch_related('contacts', 'services', 'contract', 'documents')
        #     serializer_class = VendorSerializer


        # class ServiceViewSet(viewsets.ModelViewSet):

        #     queryset = Service.objects.all()
        #     serializer_class = ServiceSerializer

        # class ContactViewSet(viewsets.ModelViewSet):
            
        #     queryset = Contact.objects.all()
        #     serializer_class = ContactSerializer


        # class ContractViewSet(viewsets.ModelViewSet):
            
        #     queryset = Contract.objects.all()
        #     serializer_class = ContractSerializer
        #     lookup_field = 'contract_number'
        #     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
        #     search_fields = ['vendor__name', 'contract_number']
        #     ordering_fields = ['contract_start_date', 'contract_expiry_date']


        # class DocumentViewSet(viewsets.ModelViewSet):
        
        #     queryset = Document.objects.all()
        #     serializer_class = DocumentSerializer

        # class VendorDetailView(RetrieveAPIView):
            
        #     queryset = Vendor.objects.all()
        #     serializer_class = VendorSerializer



class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Vendor.objects.prefetch_related('contacts', 'services', 'contract', 'documents')
        return qs if user.is_superuser else qs.filter(unit=user.unit)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, unit=self.request.user.unit)

    def perform_update(self, serializer):
        vendor = self.get_object()
        if not self.request.user.is_superuser and vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot modify vendors outside your unit.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.unit != self.request.user.unit:
            raise PermissionDenied("You cannot delete vendors outside your unit.")
        instance.delete()

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Service.objects.select_related('vendor')
        return qs if user.is_superuser else qs.filter(vendor__unit=user.unit)

    def perform_create(self, serializer):
        vendor = serializer.validated_data['vendor']
        if not self.request.user.is_superuser and vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot add services to vendors outside your unit.")
        serializer.save()

    def perform_update(self, serializer):
        service = self.get_object()
        if not self.request.user.is_superuser and service.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot modify services outside your unit.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot delete services outside your unit.")
        instance.delete()

class VendorDetailView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        vendor = super().get_object()
        user = self.request.user

        # Ensure vendor belongs to the same unit as the user
        if vendor.unit != user.unit:
            raise PermissionDenied("You do not have permission to access this vendor.")
        return vendor
    

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Contact.objects.select_related('vendor')
        return qs if user.is_superuser else qs.filter(vendor__unit=user.unit)

    def perform_create(self, serializer):
        vendor = serializer.validated_data['vendor']
        if not self.request.user.is_superuser and vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot add contacts to vendors outside your unit.")
        serializer.save()

    def perform_update(self, serializer):
        contact = self.get_object()
        if not self.request.user.is_superuser and contact.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot modify contacts outside your unit.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot delete contacts outside your unit.")
        instance.delete()

class ContractViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    lookup_field = 'contract_number'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['vendor__name', 'contract_number']
    ordering_fields = ['contract_start_date', 'contract_expiry_date']

    def get_queryset(self):
        user = self.request.user
        qs = Contract.objects.select_related('vendor')
        return qs if user.is_superuser else qs.filter(vendor__unit=user.unit)

    def perform_create(self, serializer):
        vendor = serializer.validated_data['vendor']
        if not self.request.user.is_superuser and vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot create contracts for vendors outside your unit.")
        serializer.save()

    def perform_update(self, serializer):
        contract = self.get_object()
        if not self.request.user.is_superuser and contract.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot modify contracts outside your unit.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot delete contracts outside your unit.")
        instance.delete()


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Document.objects.select_related('vendor')
        return qs if user.is_superuser else qs.filter(vendor__unit=user.unit)

    def perform_create(self, serializer):
        vendor = serializer.validated_data['vendor']
        if not self.request.user.is_superuser and vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot upload documents for vendors outside your unit.")
        serializer.save()

    def perform_update(self, serializer):
        document = self.get_object()
        if not self.request.user.is_superuser and document.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot modify documents outside your unit.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.vendor.unit != self.request.user.unit:
            raise PermissionDenied("You cannot delete documents outside your unit.")
        instance.delete()

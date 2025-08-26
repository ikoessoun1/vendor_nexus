from rest_framework import serializers
from .models import Vendor, Contract, Service, Contact, Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'vendor', 'file', 'uploaded_at']
        extra_kwargs = {'vendor': {'write_only': True}}


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'vendor', 'name', 'phone_numbers', 'email']
        extra_kwargs = {'vendor': {'write_only': True}}


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'vendor', 'name', 'shortcode', 'revenue_share']
        extra_kwargs = {'vendor': {'write_only': True}}


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'contract_number', 'vendor',
            'contract_start_date', 'contract_expiry_date',
            'contract_currency', 'contract_terms'
        ]
        extra_kwargs = {
            'vendor': {'write_only': False}
        }


class VendorSerializer(serializers.ModelSerializer):
    # Nested relationships (read-only)
    contacts = ContactSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    contract = ContractSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    #New field for user and unit
    created_by = serializers.StringRelatedField(read_only=True)
    unit = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'description', 'emails',
            'contacts', 'services', 'contract', 'documents', 'created_by', 'unit',
        ]

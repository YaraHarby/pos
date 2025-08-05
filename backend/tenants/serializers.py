from rest_framework import serializers
from .models import Tenant,Branch, Domain, Client
import re
from datetime import timedelta, date


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'tenant',
            'arabic_name',
            'english_name',
            'email',
            'phone',]
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format.")
        return value
    # def validate_phone(self, value):
    #     if not re.match(r"^\+?[0-9\s-]+$", value):
    #         raise serializers.ValidationError("Phone number must contain only digits, spaces, hyphens, and an optional leading +.")
    #     return value

class BranchSerializer(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(),
        required=False  
    )

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "tenant",
            "contact_email",
            "contact_phone",
        ]



        

class TenantSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, required=False)

    class Meta:
        model = Tenant
        fields = [
            "id",
            "arabic_name",
            "english_name",
            "Commercial_Record",
            "subdomain",
            "Subscription_Price",
            "Currency",
            "Start_Date",
            "End_Date",
            "on_trial",
            "image",
            "is_active", 
            "no_users",
            "modules_enabled", 
            "branches",
        ]
        extra_kwargs = {
            "arabic_name": {"required": False},
            "subdomain": {"required": False},
            "Commercial_Record": {"required": False},
            "Subscription_Price": {"required": False},
            "Start_Date": {"required": False},
            "End_Date": {"required": False},
        }
    def validate_arabic_name(self, value):
        if not re.match(r'^[أ-ي\s]+$', value):
            raise serializers.ValidationError("Arabic name must contain only Arabic characters and spaces.")
        return value
    
    def validate_subdomain(self, value):
        if not re.match(r'^[a-z][a-z0-9_]+$', value):
            raise serializers.ValidationError(
                "Subdomain must be lowercase, alphanumeric or underscores only, and must not start with a number."
            )
        return value
    def validate (self, attrs):
        request = self.context.get("request")
        is_partial = request and request.method == "PATCH"
        if not is_partial:
            if not attrs.get('arabic_name'):
                raise serializers.ValidationError({"arabic_name": "Arabic name is required."})
            if not attrs.get('subdomain'):
                raise serializers.ValidationError({"subdomain": "Subdomain is required."})
            if not attrs.get('Commercial_Record'):
                raise serializers.ValidationError({"Commercial_Record": "Commercial Record is required."})
            if not attrs.get('Subscription_Price'):
                raise serializers.ValidationError({"Subscription_Price": "Subscription Price is required."})

        if attrs.get('on_trial') == False:
            if not attrs.get('End_Date') and not attrs.get('Start_Date'):
                raise serializers.ValidationError("Start Date and End Date is required.")
        if attrs.get('on_trial') == True:
                attrs['Start_Date'] = attrs.get('Start_Date', date.today())
                attrs['End_Date'] = attrs['Start_Date'] + timedelta(days=14)
        return attrs

    def validate_startdate(self, attrs):
        if attrs['startdate'] < date.today():
            raise serializers.ValidationError("Start date must be in the future or today.")
        return attrs
    def validate_enddate(self, attrs):
        if attrs['enddate'] < attrs['startdate']:
            raise serializers.ValidationError("End date must be after start date.")
        if attrs['enddate'] < date.today():
            raise serializers.ValidationError("End date must be in the future.")
        if attrs['on_trial'] and (attrs['enddate'] - attrs['startdate']).days > 14:
            raise serializers.ValidationError("Trial period cannot exceed 14 days.")
        return attrs
        
    def create(self, validated_data):
        branches_data = validated_data.pop("branches", [])
        subdomain = validated_data.get("subdomain")
        
        validated_data["schema_name"] = subdomain.lower()  

        tenant = Tenant.objects.create(**validated_data)
        for branch_data in branches_data:
            Branch.objects.create(tenant=tenant, **branch_data)
        return tenant
    
    def update(self, instance, validated_data):
        """Update a tenant and its related branches."""
        branches_data = validated_data.pop("branches", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if branches_data is not None:
            existing = {b.id: b for b in instance.branches.all()}
            provided_ids = []

            for branch_data in branches_data:
                branch_id = branch_data.get("id")
                attrs = {k: v for k, v in branch_data.items() if k != "id"}

                if branch_id and branch_id in existing:
                    branch = existing[branch_id]
                    for key, value in attrs.items():
                        setattr(branch, key, value)
                    branch.save()
                    provided_ids.append(branch_id)
                else:
                    Branch.objects.create(tenant=instance, **attrs)

            # Delete branches that were not included in the payload
            for b_id, branch in existing.items():
                if b_id not in provided_ids:
                    branch.delete()

        return instance

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = "__all__"
    def validate_domain(self, value):
        if not re.match(r'^[a-z0-9-]+(\.[a-z0-9-]+)*$', value):
            raise serializers.ValidationError("Domain must be lowercase and can only contain alphanumeric characters and hyphens.")
        return value
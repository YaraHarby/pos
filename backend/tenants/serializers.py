from rest_framework import serializers
from .models import Tenant,Branch
import re

class BranchSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'parent') and isinstance(self.parent, serializers.ListSerializer):
            self.fields['tenant'].required = False

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
            "name",
            "subscription_plan",
            "contact_email",
            "contact_phone",
            "domain",
            "subdomain", 
            "paid_until",
            "on_trial",
            "modules_enabled",  # Add this line
            "branches",
        ]

    def validate_subdomain(self, value):
        if not re.match(r'^[a-z][a-z0-9_]+$', value):
            raise serializers.ValidationError(
                "Subdomain must be lowercase, alphanumeric or underscores only, and must not start with a number."
            )
        return value
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


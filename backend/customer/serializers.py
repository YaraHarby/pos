from rest_framework import serializers
from .models import Customer,Invoice,InvoiceItem,Returns_of_customer
from sales.serializers import ProductSerializer
from sales.models import Product

class customerSerializers (serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        
class InvoiceItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = InvoiceItem
        fields = ["id", "product", "product_id", "quantity"]


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ["id", "customer_name","customer_phone" ,"issue_date","due_date", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice
    


class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returns_of_customer
        fields = ["id","customer" ,"order_item", "quantity", "return_reason", "created_at"]

    def validate(self, data):
        order_item = data.get("order_item") 
        if order_item:
           
            if not order_item.is_returnable:
                raise serializers.ValidationError("This item cannot be returned.")
    
        return data

    def create(self, validated_data):
        order_item = validated_data["order_item"]
        qty_to_return = validated_data["quantity"]

        # Create return record
        ret = Returns_of_customer.objects.create(**validated_data)

        # Deduct quantity from the order item
        order_item.quantity -= qty_to_return
        if order_item.quantity == 0:
            order_item.delete()  # remove item if nothing left
        else:
            order_item.save()

        return ret
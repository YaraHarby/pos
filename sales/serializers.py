from rest_framework import serializers
from .models import Product, Supplier,OrderItem,Order,Receipt

class ProductSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Product
        fields = "__all__"
     
    def validate(self, attrs):
    
        current_stock = attrs.get('current_stock', getattr(self.instance, 'current_stock', None))
        min_stock = attrs.get('min_stock', getattr(self.instance, 'min_stock', None))

        if current_stock is not None and min_stock is not None:
            if current_stock < min_stock:
                attrs['status'] = 'Low Stock'

            else:
                attrs['status'] = 'In Stock'
            if current_stock <= 0:
                attrs['suspended'] = True

        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "seller", "status", "payment_type", "date", "items"]
        read_only_fields = ["id", "date"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item in items_data:
            product = item["product"]

            if product.current_stock < item["quantity"]:
                raise serializers.ValidationError(
                    {"detail": f"Not enough stock for {product.name}"}
                )

            product.current_stock -= item["quantity"]
            product.save()

            OrderItem.objects.create(order=order, **item)

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        # Update order main fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update items if provided
        if items_data is not None:
            for old_item in instance.items.all():
                old_item.product.current_stock += old_item.quantity
                old_item.product.save()

            instance.items.all().delete()

            for item in items_data:
                product = item["product"]
                if product.current_stock < item["quantity"]:
                    raise serializers.ValidationError(
                        {"detail": f"Not enough stock for {product.name}"}
                    )
                product.current_stock -= item["quantity"]
                product.save()
                OrderItem.objects.create(order=instance, **item)

        return instance

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = "__all__" 

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
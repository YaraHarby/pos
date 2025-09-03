from rest_framework import serializers
from .models import Product, Voucher, Supplier,OrderItem,Order,Returns_of_supplier,Receipt,PurchaseOrderItem,PurchaseOrder,Invoice,InvoiceItem

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


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'item_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['subtotal']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'supplier', 'expected_delivery', 'status', 'notes', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase_order = PurchaseOrder.objects.create(**validated_data)

        total = 0
        for item in items_data:
            subtotal = item['quantity'] * item['unit_price']
            order_item = PurchaseOrderItem.objects.create(
                purchase_order=purchase_order,
                item_name=item['item_name'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                subtotal=subtotal
            )
            total += subtotal

        purchase_order.total_amount = total
        purchase_order.save()
        return purchase_order
    

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'item_name', 'quantity', 'unit_price', 'subtotal']

    subtotal = serializers.SerializerMethodField()

    def get_subtotal(self, obj):
        return obj.subtotal()


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'supplier', 'order_id', 'issue_date', 'due_date',
            'status', 'payment_method', 'notes',
            'subtotal', 'tax', 'total',
            'items'
        ]
        read_only_fields = ['subtotal', 'total']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        invoice.calculate_totals()
        return invoice
    

class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Returns_of_supplier
        fields = ["id","supplier" ,"purchase_item", "quantity", "return_reason", "created_at"]

    def validate(self, data):
        order_item = data.get("order_item") 
        if order_item:
           
            if not order_item.is_returnable:
                raise serializers.ValidationError("This item cannot be returned.")
    
        return data

    def create(self, validated_data):
        purchase_item = validated_data["purchase_item"]
        qty_to_return = validated_data["quantity"]

        # Create return record
        ret = Returns_of_supplier.objects.create(**validated_data)

        # Deduct quantity from the order item
        purchase_item.quantity -= qty_to_return
        if purchase_item.quantity == 0:
            purchase_item.delete()  # remove item if nothing left
        else:
            purchase_item.save()

        return ret
    
class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"

    def validate(self, data):
        v_type = data.get("voucher_type")

        if v_type == "Supplier" and not data.get("supplier"):
            raise serializers.ValidationError("Supplier is required for Supplier Payment Voucher.")
        
        if v_type == "Expense" and (not data.get("category") or not data.get("recipient")):
            raise serializers.ValidationError("Category and Recipient are required for Expense Voucher.")

        return data
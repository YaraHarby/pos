# from django.db import models
# from django.contrib.postgres.fields import ArrayField
# from tenantusers.models import TenantUser

# #-----------------------------------(items)--------------------------------
# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='items/', blank=True)
#     def __str__(self):
#         return f"{self.name} {self.price}"
    
# class order (models.Model):
#     customer = models.ForeignKey(customer, on_delete=models.CASCADE)
#     seller = models.ForeignKey(TenantUser, on_delete=models.CASCADE)
#     items = ArrayField(
#         models.ForeignKey(Item, on_delete=models.CASCADE),
#         blank=True,
#     )
#     status = models.CharField(max_length=250)
#     payment_type = models.CharField(max_length=250)
#     date = models.DateTimeField(auto_now_add=True)


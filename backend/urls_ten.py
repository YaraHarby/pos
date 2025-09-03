from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path("admin/", admin.site.urls),

    path ("tenuser/",include("tenantusers.urls")), 
    path('seller/', include('sales.urls')),
    path('customer/', include('customer.urls')),


]
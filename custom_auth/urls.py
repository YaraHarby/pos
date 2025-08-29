from django.urls import path, include
from . import views_saas

urlpatterns = [
    path("saas/login/", views_saas.Saaslogin, name="saas_login"),
    path("saas/me/", views_saas.saasprofile, name="saas_profile"),
    path('saas/addadmin/',views_saas.add_saasadmin.as_view(),name ="add saas admin"),
    path('saas/users/',views_saas.listadmins.as_view()),
    path('saas/updateuser/<id>/',views_saas.update_user),
    path('saas/getuser/<id>/',views_saas.get_saasuser),
    path('saas/deleteuser/<id>/',views_saas.delete_user),
    path('saas/logout/',views_saas.logout_view),
    path('saas/deletemyaccount/',views_saas.delete_account),
    path('saas/updateprofile/',views_saas.update_profile),
    path('saas/addtenantusers/', views_saas.CreateTenantUserFromSaaS.as_view(), name='create-tenant-user-from-saas'),


    
    # path('saas/listtenantusers/', views_saas.TenantUserListView.as_view(), name='tenant_user_list'),


]
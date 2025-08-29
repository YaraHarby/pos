from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,AbstractUser
# from tenants.models import Tenant

# Create your models here.
class SaasUseraManager(BaseUserManager):
    def create_user(
        self, email, username, password=None, **extra_fields
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(
        self, email, username, password=None
    ):
        user = self.create_user(
            email,
            username=username,
            password=password,
            is_admin=True,
            is_superuser=True,
        )
        return user


class SaasUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    Age = models.CharField(max_length=500, default='',null=True, blank=True)
    Gender = models.CharField(max_length=500, default='',null=True, blank=True)
    Address = models.CharField(max_length=500, default='',null=True, blank=True)
    is_superuser = models.BooleanField(default=True, null=True, blank=True)
    objects = SaasUseraManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app app_label?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class RefreshTokenStore(models.Model):
    user = models.ForeignKey(SaasUser, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}"


# class Profile(models.Model):
#     user = models.OneToOneField(SaasUser, on_delete=models.CASCADE)
#     reset_password_token = models.CharField(max_length=50, blank=True, null=True)

#     def __str__(self):
#         return self.user.username
    

# class TenantUser (AbstractUser):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(
#         verbose_name="Email",
#         max_length=255,
#         unique=True,
#     )
   
#     ROLE_CHOICES = [
#         ("ROLE_MANAGER", 'Manager'),
#         ("ROLE_SALES", 'Sales'),
#         ("ROLE_DELIVERY", 'Delivery'),
#         ("ROLE_KITCHEN", 'Kitchen'),
#     ]
    
#     UserID = models.CharField(max_length=10, unique=True, blank=True)
#     Age = models.CharField(max_length=500, default='',null=True, blank=True)
#     Gender = models.CharField(max_length=500, default='',null=True, blank=True)
#     Address = models.CharField(max_length=500, default='',null=True, blank=True)
#     tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
#     branch = models.ForeignKey('tenants.Branch', null=True, blank=True, on_delete=models.SET_NULL)

#     role = models.CharField(
#         max_length=30, choices=ROLE_CHOICES, default="Sales"
#     )
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return self.is_authenticated



    
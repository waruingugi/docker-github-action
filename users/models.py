from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class SimpleUserManager(BaseUserManager):
    def create_user(
        self,
        *,
        email,
        password,
        **extra_fields
    ):
        """Create and save a user with the given email and password"""
        if not email:
            raise ValueError(_("User must provide an email address."))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, *, email, password, **extra_fields):
        """Create and save a superuser with the given email and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True"))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True"))
        
        return self.create_user(email=email, password=password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    email = models.EmailField(_("Email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    email_is_verified = models.BooleanField(
        _("Email is verified"),
        default=False,
        help_text=_("Is the user email verified")
    )

    objects = SimpleUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

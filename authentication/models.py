from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


USER_TYPE = [
    ('sales_representative', 'Sales Representative'),
    ('sales_admin', 'Sales Admin'),
]


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.approval_status_pending = False
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    created_at = models.DateTimeField(default=timezone.now)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    phonenumber = models.IntegerField(blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="user_avatar/")
    user_type = models.CharField(max_length=20, choices=USER_TYPE)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    approval_status_pending = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def __str__(self):
        return self.firstname

    def __str__(self):
        return self.lastname

    def __str__(self):
        full_name = '%s %s' % (self.firstname, self.lastname)
        return full_name.strip()

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "static/images/avatar1.jpg"

    def get_approval_status(self):
        return self.approval_status_pending

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        permissions = (
            ("add_leads", "To add leads"),
            ("edit_leads", "To edit leads"),
            ("delete_leads", "To delete leads"),
            ("view_leads", "To view leads"),
            ("assign_leads", "To assign leads to sales representatives")
        )

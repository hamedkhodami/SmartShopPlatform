from apps.core.models import BaseModel
from apps.core.utils import get_coded_phone_number
from apps.core.validators import OnlyPersianCharsValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .auth.utils import is_melli_code
from .enums import UserGenderEnum, UserRoleEnum
from .managers import CustomObjectsManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):

    Role = UserRoleEnum

    phone_number = PhoneNumberField(
        region="IR", unique=True, verbose_name=_("Phone number")
    )
    email = models.EmailField(_("Email"), max_length=225, null=True, blank=True)
    first_name = models.CharField(
        _("First name"),
        max_length=128,
        null=True,
        blank=True,
        default=_("No Name"),
        validators=[OnlyPersianCharsValidator],
    )
    last_name = models.CharField(
        _("Last name"),
        max_length=128,
        null=True,
        blank=True,
        default=_("No Name"),
        validators=[OnlyPersianCharsValidator],
    )
    role = models.CharField(
        _("Role"), max_length=20, choices=Role.choices, default=Role.VIEWER
    )
    national_id = models.CharField(
        _("National id"),
        max_length=11,
        unique=True,
        validators=[MinLengthValidator(9), MaxLengthValidator(11)],
    )

    is_phone_number_confirmed = models.BooleanField(default=False)
    is_national_id_confirmed = models.BooleanField(default=False)

    is_active = models.BooleanField(_("Active"), default=True)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_staff = models.BooleanField(_("Staff"), default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomObjectsManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.phone_number} - {self.email or 'No Email'}"

    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or _("No Name")

    @property
    def is_blocked(self):
        try:
            return bool(self.userblock)
        except ObjectDoesNotExist:
            return False

    def has_role(self, role_name):
        return self.role == role_name

    @property
    def is_store_admin_user(self):
        return self.has_role("store_admin")

    @property
    def raw_phone_number(self):
        return get_coded_phone_number(self.phone_number)

    def national_id_check(self, phone_number, national_id):
        if not is_melli_code(national_id):
            return False

        user = User.objects.filter(
            phone_number=phone_number, national_id=national_id
        ).first()
        return user is not None

    def national_id_check_by_data(self, phone_number, national_id):
        if not is_melli_code(national_id):
            return False

        if self.phone_number != phone_number or self.national_id != national_id:
            return False

        return True


class UserProfileModel(BaseModel):

    Gender = UserGenderEnum

    user = models.OneToOneField(
        User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="profile"
    )
    gender = models.CharField(
        _("Gender"), max_length=10, choices=Gender.choices, null=True, blank=True
    )
    bio = models.TextField(_("Bio"), blank=True, null=True)
    image = models.ImageField(
        _("Picture"), upload_to="images/profiles/", null=True, blank=True
    )
    city = models.CharField(_("City"), max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("Users profile")

    def __str__(self):
        return f"{self.user}"


class UserBlock(BaseModel):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="userblock"
    )
    admin = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_blocked_by_admin",
    )
    note = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Blocked User")
        verbose_name_plural = _("Blocked Users")

    def __str__(self):
        return f"{self.user}"

    def is_blocked_by_admin(self, admin_user):
        return self.admin == admin_user

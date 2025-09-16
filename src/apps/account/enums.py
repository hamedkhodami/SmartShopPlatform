from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserRoleEnum(TextChoices):

    ADMIN = "admin", _("Admin")
    STORE_ADMIN = "store_admin", _("Store Admin")
    CUSTOMER = "customer", _("Customer")
    VIEWER = "viewer", _("Viewer")


class UserGenderEnum(TextChoices):

    MALE = "m", _("Male")
    FEMALE = "f", _("Female")

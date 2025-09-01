import re

from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class OnlyPersianCharsValidator:
    message = _("Ensure character are persian")
    code = "only_persian_chars"
    persian_regex = re.compile(
        r"^[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\s\d۰-۹]+$"
    )

    def __call__(self, value):
        if not self.persian_regex.match(value):
            raise ValidationError(self.message, code=self.code)

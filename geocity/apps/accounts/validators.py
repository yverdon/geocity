from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


def validate_email(value):
    try:
        EmailValidator()(value)
        return True
    except ValidationError:
        return False

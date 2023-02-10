from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


def due_back_validator(due_back):
    if  datetime.date.today() > due_back:
        raise ValidationError(
            _('%(due_back)s is in past!'),
            params={'due_back': due_back},
        )

    if datetime.date.today() + datetime.timedelta(weeks=4) < due_back:
        raise ValidationError(
            _('%(due_back)s is more than 4 weeks!'),
            params={'due_back': due_back},
        )

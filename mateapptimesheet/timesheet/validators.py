from django.core.exceptions import ValidationError
from datetime import date
from django.utils.translation import gettext_lazy as _

today = date.today()

def invalidate_future_timesheets(timeDate):
    if timeDate > today:
        raise ValidationError(_("You can't log timesheets in a future date."))
    else:
        return timeDate

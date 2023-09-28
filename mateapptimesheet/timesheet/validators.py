from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _

tomorrow = date.today() + timedelta(days=1)

def invalidate_future_timesheets(timeDate):
    if timeDate >= tomorrow:
        raise ValidationError(_("You can't log timesheets in a future date."))
    else:
        return timeDate

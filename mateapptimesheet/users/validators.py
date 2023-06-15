from django.core.exceptions import ValidationError

def validate_email_domain(email):
    if not '@alphaworks.com.ar' in email:
        raise ValidationError('Only @alphaworks.com.ar mails are accepted.')
    else:
        return email

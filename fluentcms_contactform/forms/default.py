from .base import AbstractContactForm
from fluentcms_contactform import appsettings
from ..models import ContactFormData


class ContactForm(AbstractContactForm):
    """
    A simple contact form, backed by a model to save all data (in case email fails).
    """

    class Meta:
        model = ContactFormData
        fields = appsettings.FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS

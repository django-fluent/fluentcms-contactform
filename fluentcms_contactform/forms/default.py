from fluentcms_contactform import appsettings
from .base import AbstractContactForm, ContactFormHelper, SubmitButton
from ..models import ContactFormData


class ContactForm(AbstractContactForm):
    """
    A simple contact form, backed by a model to save all data (in case email fails).
    """

    class Meta:
        model = ContactFormData
        fields = appsettings.FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS

    helper = ContactFormHelper()
    helper.add_input(SubmitButton())

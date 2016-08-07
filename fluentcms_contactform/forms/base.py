from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from .. import appsettings
from ..email import send_contact_form_email
from ..utils import get_remote_ip

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict


class SubmitButton(Submit):
    """
    The submit button to add to the layout.

    Note: the ``contactform_submit`` is mandatory, it helps the
    """

    def __init__(self, text=_("Submit"), **kwargs):
        super(SubmitButton, self).__init__(name='contactform_submit', value=text, **kwargs)


class ContactFormHelper(FormHelper):
    """
    The django-crispy-forms configuration that handles form appearance.
    The default is configured to show bootstrap forms nicely.
    """
    form_tag = True
    form_class = appsettings.FLUENTCMS_CONTACTFORM_FORM_CSS_CLASS
    label_class = appsettings.FLUENTCMS_CONTACTFORM_LABEL_CSS_CLASS
    field_class = appsettings.FLUENTCMS_CONTACTFORM_FIELD_CSS_CLASS


class PrefillUserMixin(object):
    """
    A mixin to prefill the user name + email fields.
    """
    user = None

    def __init__(self, data=None, *args, **kwargs):
        if self.user is not None and self.user.is_authenticated():
            self.prefill_user_fields(self.user)

    def prefill_user_fields(self, user):
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.initial.update({
            'email': self.user.email,
            'name': self.user.get_full_name() or self.user.username
        })

    def clean_email(self):
        if self.user is not None and self.user.is_authenticated():
            return self.initial['email']
        return self.cleaned_data['email']

    def clean_name(self):
        if self.user is not None and self.user.is_authenticated():
            return self.initial['name']
        return self.cleaned_data['name']


class AbstractContactForm(forms.ModelForm):
    """
    Base class for model forms.
    """
    hide_summary_fields = ('captcha',)

    #: The form helper to override. This makes sure that form-horizontal is properly rendered.
    #: The form tag is disabled on purpose, so the regular form rendering works as expected.
    helper = ContactFormHelper()
    helper.form_tag = False

    def __init__(self, data=None, *args, **kwargs):
        # Support receiving a user argument.
        self.user = kwargs.pop('user', None)
        super(AbstractContactForm, self).__init__(data, *args, **kwargs)
        if 'phone_number' in self.fields:
            self.fields['phone_number'].widget.input_type = 'tel'

    def get_field_summary(self):
        """
        Provide the submitted data in a user readable way.
        :returns: An ordered dict of fields with their label + value.
        :rtype: collections.OrderedDict
        """
        return OrderedDict([
            (force_text(field.label), field.value()) for field in self.visible_fields() if field.name not in self.hide_summary_fields
        ])

    def submit(self, request, email_to, style='default'):
        """
        Store data in database and submit the email.
        The database store avoids loosing contact information.
        """
        self.instance.ip_address = get_remote_ip(request)
        self.save()

        # Send email with information too.
        send_contact_form_email(self, request, email_to, style=style)

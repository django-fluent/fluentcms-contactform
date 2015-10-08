from django import forms
from ..email import send_contact_form_email
from ..utils import get_remote_ip

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict


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

    def __init__(self, data=None, *args, **kwargs):
        # Support receiving a user argument.
        self.user = kwargs.pop('user', None)
        super(AbstractContactForm, self).__init__(data, *args, **kwargs)

    def get_field_summary(self):
        """
        Provide the submitted data in a user readable way.
        :returns: An ordered dict of fields with their label + value.
        :rtype: collections.OrderedDict
        """
        return OrderedDict([
            (unicode(field.label), field.value()) for field in self.visible_fields() if field.name not in self.hide_summary_fields
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


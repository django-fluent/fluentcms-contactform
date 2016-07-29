"""

"""
from crispy_forms.layout import Layout, Row, Column
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from fluentcms_contactform import appsettings
from fluentcms_contactform.forms.base import AbstractContactForm, ContactFormHelper, SubmitButton
from fluentcms_contactform.models import ContactFormData


class CompactContactForm(AbstractContactForm):
    """
    A form with a very compact layout;
    all the name/email/phone fields are displayed in a single top row.
    It uses Bootstrap 3 layout by default to generate the columns.

    For improved appearance, disable the "subject" line too using::

        FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS = ('name', 'email', 'phone_number', 'message')
    """
    top_row_fields = appsettings.FLUENTCMS_CONTACTFORM_COMPACT_FIELDS
    top_row_columns = appsettings.FLUENTCMS_CONTACTFORM_COMPACT_GRID_SIZE
    top_column_class = appsettings.FLUENTCMS_CONTACTFORM_COMPACT_COLUMN_CSS_CLASS

    class Meta:
        model = ContactFormData
        fields = appsettings.FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS

    @cached_property
    def helper(self):
        # As extra service, auto-adjust the layout based on the project settings.
        # This allows defining the top-row, and still get either 2 or 3 columns
        top_fields = [name for name in self.fields.keys() if name in self.top_row_fields]
        other_fields = [name for name in self.fields.keys() if name not in self.top_row_fields]
        col_size = int(self.top_row_columns / len(top_fields))
        col_class = self.top_column_class.format(size=col_size)

        helper = ContactFormHelper()
        helper.form_class = 'form-vertical contactform-compact'
        helper.label_class = 'sr-only'
        helper.field_class = ''
        helper.layout = Layout(
            Row(*[Column(name, css_class=col_class) for name in top_fields]),
            *other_fields
        )
        helper.add_input(SubmitButton())
        return helper

    def __init__(self, *args, **kwargs):
        super(CompactContactForm, self).__init__(*args, **kwargs)
        if 'phone_number' in self.fields:
            self.fields['phone_number'].label = _("Phone")

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = u"{0}:".format(field.label)

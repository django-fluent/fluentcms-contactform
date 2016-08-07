from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from fluent_contents.models import ContentItem
from phonenumber_field.modelfields import PhoneNumberField
from . import appsettings
from .compat import lru_cache
from .utils import import_symbol


class AbstractContactFormData(models.Model):
    """
    The base internal fields to save for every contact form.
    """
    # Internal data
    submit_date = models.DateTimeField(_("Submit date"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    internal_note = models.TextField(_('Internal Notes'), blank=True)
    is_archived = models.BooleanField(_('Archived'), db_index=True, default=False, blank=True,
                                      help_text=_("Mark the form as archived when the e-mail has been handled."))

    class Meta:
        abstract = True
        ordering = ('submit_date',)
        verbose_name = _("Contact form data")
        verbose_name_plural = _("Contact form data")


@python_2_unicode_compatible
class ContactFormData(AbstractContactFormData):
    """
    Visitor-submitted form data.
    """
    # Submitted data
    name = models.CharField(_('Name'), max_length=200)
    email = models.EmailField(_('Email'), max_length=200)
    phone_number = PhoneNumberField(_("Phone number"), blank=True, null=True)
    subject = models.CharField(_('Subject'), max_length=200, default='')
    message = models.TextField(_('Message'))

    class Meta:
        ordering = ('submit_date',)
        verbose_name = _("Contact form data")
        verbose_name_plural = _("Contact form data")

    def __str__(self):
        return u'{0}'.format(self.subject or self.email)


@python_2_unicode_compatible
class ContactFormItem(ContentItem):
    """
    Plugin definition
    """
    form_style = models.CharField(_("Form"), max_length=100, choices=appsettings.FORM_STYLE_CHOICES)
    email_to = models.EmailField(_("Email to"), max_length=200,
                                 help_text=_("The email address where submitted forms should be sent to."))
    success_message = models.TextField(_("Thank you message"))

    class Meta:
        verbose_name = _("Contact form")
        verbose_name_plural = _("Contact form")

    def __str__(self):
        return self.email_to

    def get_form_class(self):
        return _get_form_class(self.form_style)


@lru_cache()
def _get_form_class(form_style):
    # Load and cache the form class.
    style = get_form_style_settings(form_style)
    return import_symbol(style['form_class'])


def get_form_style_settings(form_style):
    """
    Return the metadata of a form style.
    """
    for key, style in appsettings.FLUENTCMS_CONTACTFORM_STYLES:
        if key == form_style:
            return style
    raise ImproperlyConfigured("No FLUENTCMS_CONTACTFORM_STYLES defined for '{0}'".format(form_style))

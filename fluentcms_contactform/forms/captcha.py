from __future__ import absolute_import
from django.utils.translation import pgettext_lazy
from .default import DefaultContactForm

try:
    from captcha.fields import CaptchaField
except ImportError:
    raise ImportError("To use {0}, you need to have django-simple-captcha installed.".format(__name__))


class CaptchaContactForm(DefaultContactForm):
    """
    Contact form with captcha field.
    """
    captcha = CaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))

from __future__ import absolute_import
from django.utils.translation import pgettext_lazy
from .default import DefaultContactForm

try:
    from captcha.fields import ReCaptchaField
except ImportError:
    raise ImportError("To use {0}, you need to have django-recaptcha installed.".format(__name__))


class ReCaptchaContactForm(DefaultContactForm):
    """
    Contact form with reCAPTCHA field.
    """
    captcha = ReCaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))

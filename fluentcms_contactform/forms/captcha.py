from django.utils.translation import pgettext_lazy

from .default import DefaultContactForm

try:
    from captcha.fields import CaptchaField
except ImportError:
    raise ImportError(f"To use {__name__}, you need to have django-simple-captcha installed.")


class CaptchaContactForm(DefaultContactForm):
    """
    Contact form with captcha field.
    """

    captcha = CaptchaField(help_text=pgettext_lazy("captcha-help-text", "Type the text."))

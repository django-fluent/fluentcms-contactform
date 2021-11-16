from django.utils.translation import pgettext_lazy

from .default import DefaultContactForm

try:
    from captcha.fields import ReCaptchaField
except ImportError:
    raise ImportError(f"To use {__name__}, you need to have django-recaptcha installed.")


class ReCaptchaContactForm(DefaultContactForm):
    """
    Contact form with reCAPTCHA field.
    """

    captcha = ReCaptchaField(help_text=pgettext_lazy("captcha-help-text", "Type the text."))

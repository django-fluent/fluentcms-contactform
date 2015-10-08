from django.utils.translation import pgettext_lazy
from .default import ContactForm

try:
    from captcha.fields import CaptchaField
except ImportError:
    raise ImportError("To use {0}, you need to have django-simple-captcha installed.\nUse: pip install django-simple-captcha".format(__name__))


class CaptchaContactForm(ContactForm):
    """
    Contact form with captcha field.
    """
    captcha = CaptchaField(help_text=pgettext_lazy("captcha-help-text", u"Type the text."))
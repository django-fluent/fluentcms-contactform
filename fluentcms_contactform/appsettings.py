from django.conf import settings
from django.utils.translation import ugettext_lazy as _


FLUENTCMS_CONTACTFORM_STYLES = (
    ('default', {
        'title': _("Default"),
        'form_class': 'fluentcms_contactform.forms.default.ContactForm',
    }),
    ('captcha', {
        'title': _("Default with captcha"),
        'form_class': 'fluentcms_contactform.forms.captcha.CaptchaContactForm',
    }),
)


# The site name in the from "Name via Site" addressing
FLUENTCMS_CONTACTFORM_VIA = getattr(settings, 'FLUENTCMS_CONTACTFORM_VIA', None)

# Allow to configure which fields to show in the default form.
FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS = getattr(settings, 'FLUENTCMS_CONTACTFORM_DEFAULT_FIELDS', ('name', 'email', 'phone_number', 'subject', 'message'))

# The possible contact form styles the user can choose
FLUENTCMS_CONTACTFORM_STYLES = getattr(settings, 'FLUENTCMS_CONTACTFORM_STYLES', FLUENTCMS_CONTACTFORM_STYLES)

# The IP address resolving function, defaults to django-ipware's public IP address detection
FLUENTCMS_CONTACTFORM_IP_RESOLVER = getattr(settings, 'FLUENTCMS_CONTACTFORM_IP_RESOLVER', 'ipware.ip.get_real_ip')

# Internal variable exposed via settings
FORM_STYLE_CHOICES = [(key, style['title']) for key, style in FLUENTCMS_CONTACTFORM_STYLES]

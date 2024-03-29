from email.utils import formataddr

import django
from django.conf import settings
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from fluentcms_contactform import appsettings


def send_contact_form_email(contactform, request, email_to, style="default"):
    """
    Send an email notification message.
    :type contactform: fluentcms_contactform.forms.base.AbstractContactForm
    :type request: HttpRequest
    :type email_to: str
    """
    message = MessageFactory(request).get_message(contactform, email_to, style=style)
    message.send()


class MessageFactory:
    """
    Generate a contact email.

    This class is purposely split in in many small pieces
    so parts are easily reusable to send custom contact emails.
    """

    text_template_name = "fluentcms_contactform/staff_email/{style}.txt"

    def __init__(self, request):
        """
        :type request: HttpRequest
        :type form: fluentcms_contactform.forms.base.AbstractContactForm
        """
        self.request = request
        self.site = get_current_site(self.request)

    def get_message(self, form, email_to, style="default", **extra_context):
        """
        Generate an email notification message.
        :type email_to: str
        """
        email_context = self.get_email_context(form, **extra_context)
        user_name = self.get_user_name(form)
        user_email = self.get_user_email(form)

        email_from = self.get_email_from(user_name, user_email)
        headers = self.get_email_headers(user_name, user_email)

        subject = self.render_subject(form)
        email_txt = self.render_text_message(email_context, style)
        return EmailMessage(subject, email_txt, email_from, to=[email_to], headers=headers)

    def get_user_name(self, form):
        return form.cleaned_data["name"]

    def get_user_email(self, form):
        return form.cleaned_data["email"]

    def get_email_context(self, form, **extra_context):
        """
        Generate the context data for the template
        """
        db_data = form.instance
        context = {
            "request": self.request,
            "site": self.site,
            "db_data": db_data,
            "admin_form_data_url": self.get_admin_url(db_data),
            "form_data": form.get_field_summary(),
        }
        context.update(extra_context)
        return context

    def get_admin_url(self, object):
        """
        Generate the admin URL for an object.
        """
        current_app = self.request.resolver_match.namespace
        url = reverse(
            admin_urlname(object._meta, "change"), args=(object.pk,), current_app=current_app
        )
        return f"http://{self.site.domain}{url}"

    def get_email_from(self, user_name, user_email):
        """
        Format the from address.
        This uses ``DEFAULT_FROM_EMAIL`` by default to avoid spam detection (e.g. SPF).
        A ``Reply-To`` header should be added to handle direct email replies.
        """
        via = appsettings.FLUENTCMS_CONTACTFORM_VIA or self.site.name
        return formataddr((f"{user_name} via {via}", settings.DEFAULT_FROM_EMAIL))

    def get_email_headers(self, user_name, user_email):
        """
        Return any additional email headers.
        This includes the ``Reply-To`` header to accompany the default "via" format in :meth:`get_email_from`.
        """
        # Avoid spam detection: http://stackoverflow.com/a/14555043/146289
        # From: Name via Site <info@example.org>
        # To: info@example.org
        # Reply-To: Name <email>
        return {
            "Reply-To": formataddr((user_name, user_email)),
        }

    def render_subject(self, form):
        """
        Render the subject.
        """
        try:
            return _("Contact form submitted by '{name}'").format(name=self.get_user_name(form))
        except KeyError:
            # Don't fail when translations are broken.
            return f"Contact form submitted by '{self.get_user_name(form)}'"

    def render_text_message(self, email_context, style="default"):
        """
        Render a plain text message.
        """
        template_names = [
            self.text_template_name.format(style=style),
            self.text_template_name.format(style="default"),
        ]
        return render_txt_template(template_names, email_context)


def render_txt_template(template_name, context):
    """
    Render a plain text template without escaping variables to HTML.

    .. note::
        This is only supported for Django 1.10 and below,
        thus exists for backwards compatibility.
    """
    if django.VERSION >= (1, 10):
        # Can't disable autoescaping anymore!
        # It's a backend engine setting now.
        return render_to_string(template_name, context)
    else:
        # For backwards compatibility
        return render_to_string(template_name, context, context_instance=Context(autoescape=False))

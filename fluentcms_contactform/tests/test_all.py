from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.test import RequestFactory
from django.test import TestCase
from django.core import mail
from fluent_contents.extensions import HttpRedirectRequest
from fluent_contents.tests.factories import create_content_item
from fluent_contents.tests.utils import render_content_items

from fluentcms_contactform.email import send_contact_form_email
from fluentcms_contactform.forms import DefaultContactForm
from fluentcms_contactform.models import ContactFormItem, ContactFormData


def get_dummy_request(method='get', **kwargs):
    """
    Returns a Request instance populated with cms specific attributes.
    """
    factory = RequestFactory()
    method = getattr(factory, method)

    request = method("/", HTTP_HOST='example.org', **kwargs)
    request.session = {}
    request.LANGUAGE_CODE = settings.LANGUAGE_CODE
    request.user = AnonymousUser()
    return request


class ContactFormTests(TestCase):
    """
    Testing private notes
    """

    def test_rendering(self):
        """
        Test the standard button
        """
        item = create_content_item(ContactFormItem, pk=1, form_style='default', email_to='testresult@example.org', success_message='Thanks!')
        output = render_content_items([item])

        self.assertTrue(output.html.count('<form '), 1)  # no helper!
        self.assertTrue(output.html.count('<input type="submit"'), 1)  # button found!
        self.assertTrue(output.html.count('name="contact1_submit"'), 1)  # button text
        self.assertEqual(str(item), 'testresult@example.org')

    def test_submit(self):
        """
        Testing submit
        """
        item = create_content_item(ContactFormItem, pk=2, form_style='default', email_to='testresult@example.org', success_message='Thanks!')

        # Submit, but not via the form button
        request = get_dummy_request('post', data={})
        request.resolver_match = resolve('/admin/')
        output = render_content_items([item], request=request)

        self.assertTrue(output.html.count('name="contact2_submit"'), 1)  # still displays form
        self.assertTrue('error' not in output.html)  # no errors!

        # Submit, but not via the form button
        request = get_dummy_request('post', data={
            'contact2-name': "Test",
            'contact2-email': 'test@example.org',
            'contact2-phone_number': '',
            'contact2-subject': 'Test!',
            'contact2-message': "Hello!",
            'contact2_submit': "Submit",
        })
        request.resolver_match = resolve('/admin/')

        self.assertRaises(HttpRedirectRequest, lambda: render_content_items([item], request=request))
        self.assertTrue(request.session['contact2_submitted'])

    def test_email(self):
        """
        Test rendering the email
        """
        contactform = DefaultContactForm(
            data={
                'name': "Test",
                'email': 'test@example.org',
                'phone_number': '',
                'subject': 'Test!',
                'message': "Hello!",
            }
        )
        self.assertTrue(contactform.is_valid())

        request = get_dummy_request()
        request.resolver_match = resolve('/admin/')
        send_contact_form_email(contactform, request, 'testresult@example.org')

        email = mail.outbox[0].body
        self.assertTrue('Message: Hello!' in email)

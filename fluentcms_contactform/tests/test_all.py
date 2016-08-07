from django.test import TestCase
from fluent_contents.tests.factories import create_content_item
from fluent_contents.tests.utils import render_content_items
from fluentcms_contactform.models import ContactFormItem


class ContactFormTests(TestCase):
    """
    Testing private notes
    """

    def test_rendering(self):
        """
        Test the standard button
        """
        item = create_content_item(ContactFormItem, form_style='default', email_to='test@example.org', success_message='Thanks!')
        output = render_content_items([item])

        self.assertTrue(output.html.count('<form '), 1)  # no helper!
        self.assertTrue(output.html.count('<input type="submit"'), 1)  # button found!
        self.assertTrue(output.html.count('name="contact1_submit"'), 1)  # button text
        self.assertEqual(str(item), 'test@example.org')

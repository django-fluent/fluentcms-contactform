from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import plugin_pool, ContentPlugin
from .models import ContactFormItem


@plugin_pool.register
class ContactFormPlugin(ContentPlugin):
    """
    Plugin to render and process a contact form.
    """
    model = ContactFormItem
    category = _("Media")
    render_template = "fluentcms_contactform/forms/{style}.html"
    render_ignore_item_language = True
    cache_output = False
    submit_button_name = 'contactform_submit'

    formfield_overrides = {
        'success_message': {
            'widget': AdminTextareaWidget(attrs={'rows': 4})
        }
    }

    def get_render_template(self, request, instance, **kwargs):
        """
        Support different templates based on the ``form_style``.
        """
        return [
            self.render_template.format(style=instance.form_style),
            self.render_template.format(style='base'),
        ]


    def render(self, request, instance, **kwargs):
        """
        Render the plugin, process the form.
        """
        context = self.get_context(request, instance, **kwargs)
        context['completed'] = False

        ContactForm = instance.get_form_class()
        if request.method == 'POST':
            # Allow multiple forms at the same page.
            if not self.submit_button_name or self.submit_button_name in request.POST:
                form = ContactForm(request.POST, request.FILES, user=request.user, prefix='contact')
            else:
                form = ContactForm(initial=request.POST, user=request.user, prefix='contact')

            if form.is_valid():
                # Submit the email, save the data in the database.
                form.submit(request, instance.email_to, style=instance.form_style)

                # Request a redirect
                # TODO: offer option to redirect to a different page.
                request.session['fluentcms_contactform_completed'] = True
                return self.redirect(request.path)
        else:
            form = ContactForm(user=request.user, prefix='contact')

            # Show completed message
            if request.session.get('fluentcms_contactform_completed'):
                del request.session['fluentcms_contactform_completed']
                context['completed'] = True

        context['form'] = form
        template = self.get_render_template(request, instance, **kwargs)
        return self.render_to_string(request, template, context)

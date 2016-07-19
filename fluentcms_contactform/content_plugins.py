from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import plugin_pool, ContentPlugin, ContentItemForm

from fluentcms_contactform.forms.base import SubmitButton
from .models import ContactFormItem, get_form_style_settings
from .utils import import_symbol


class ContactFormItemForm(ContentItemForm):
    """
    Validate the contact form.
    """

    def clean_form_style(self):
        """
        Check whether the style can be used, to avoid frontend errors.
        """
        form_style = self.cleaned_data['form_style']
        style_settings = get_form_style_settings(form_style)

        # Verify whether the style can be used
        for app in style_settings.get('required_apps', ()):
            if app not in settings.INSTALLED_APPS:
                msg = _("This form style can't be used, it requires the '{0}' app to be installed.")
                raise ValidationError(msg.format(app))

        try:
            import_symbol(style_settings['form_class'])
        except (ImportError, ImproperlyConfigured, AttributeError) as e:
            msg = _("This form style can't be used, not all required libraries are installed.\n{0}")
            raise ValidationError(msg.format(str(e)))

        return form_style


@plugin_pool.register
class ContactFormPlugin(ContentPlugin):
    """
    Plugin to render and process a contact form.
    """
    model = ContactFormItem
    form = ContactFormItemForm
    category = _("Media")
    render_template = "fluentcms_contactform/forms/{style}.html"
    render_ignore_item_language = True
    cache_output = False
    submit_button_name = 'contact{pk}_submit'

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
        # Allow multiple forms at the same page.
        prefix = 'contact{0}'.format(instance.pk)
        submit_button_name = self.submit_button_name.format(pk=instance.pk)
        session_data_key = 'contact{0}_submitted'.format(instance.pk)

        # Base context
        context = self.get_context(request, instance, **kwargs)
        context['submit_button_name'] = submit_button_name
        context['completed'] = False

        ContactForm = instance.get_form_class()
        if request.method == 'POST':
            if submit_button_name in request.POST or 'contactform_submit' in request.POST:
                form = ContactForm(request.POST, request.FILES, user=request.user, prefix=prefix)
            else:
                form = ContactForm(initial=request.POST, user=request.user, prefix=prefix)

            if form.is_valid():
                # Submit the email, save the data in the database.
                form.submit(request, instance.email_to, style=instance.form_style)

                # Request a redirect.
                # Use the session temporary so results are shown at the next GET call.
                # TODO: offer option to redirect to a different page.
                request.session[session_data_key] = True
                return self.redirect(request.path)
        else:
            form = ContactForm(user=request.user, prefix=prefix)

            # Show completed message
            if request.session.get(session_data_key):
                del request.session[session_data_key]
                context['completed'] = True

        if hasattr(form, 'helper') and form.helper.inputs:
            # Hacky, when using crispy layouts, make sure the button name is set.
            # In case this fails, the code above also checks for the general 'contactform_submit' name.
            submit_buttons = [input for input in form.helper.inputs if isinstance(input, SubmitButton)]
            if submit_buttons:
                submit_buttons[0].name = submit_button_name

        context['form'] = form
        template = self.get_render_template(request, instance, **kwargs)
        return self.render_to_string(request, template, context)

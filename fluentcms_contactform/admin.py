from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.translation import ugettext_lazy as _
from .forms.default import DefaultContactForm
from .models import ContactFormData


FORM_DATA_FIELDS = tuple(DefaultContactForm.base_fields.keys())


class ContactFormDataAdmin(admin.ModelAdmin):
    """
    Administrate the submitted contact form data.
    """
    list_display = ('name', 'email', 'is_archived', 'submit_date')
    list_filter = ('is_archived',)
    date_hierarchy = 'submit_date'
    search_fields = FORM_DATA_FIELDS
    actions = ('archive_entries',)

    fieldsets = (
        (None, {
            'fields': FORM_DATA_FIELDS,
            'classes': ('wide',),
        }),
        (_("Staff information"), {
            'fields': ('submit_date', 'ip_address', 'internal_note', 'is_archived'),
            'classes': ('wide',),
        })
    )
    readonly_fields = FORM_DATA_FIELDS + ('submit_date', 'ip_address')

    def has_add_permission(self, *args, **kwargs):
        return False

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'internal_note':
            kwargs['widget'] = AdminTextareaWidget(attrs={'rows': 4})
        return super(ContactFormDataAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def archive_entries(self, request, queryset):
        queryset.update(is_archived=True)

    archive_entries.short_description = _("Archive selected entries")


admin.site.register(ContactFormData, ContactFormDataAdmin)

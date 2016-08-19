# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import fluentcms_contactform.appsettings


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactFormData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submit_date', models.DateTimeField(auto_now_add=True, verbose_name='Submit date')),
                ('ip_address', models.GenericIPAddressField(null=True, verbose_name='IP address', blank=True)),
                ('internal_note', models.TextField(verbose_name='Internal Notes', blank=True)),
                ('is_archived', models.BooleanField(default=False, help_text='Mark the form as archived when the e-mail has been handled.', db_index=True, verbose_name='Archived')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('email', models.EmailField(max_length=200, verbose_name='Email')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='Phone number', blank=True)),
                ('subject', models.CharField(max_length=200, verbose_name='Subject', default='')),
                ('message', models.TextField(verbose_name='Message')),
            ],
            options={
                'ordering': ('submit_date',),
                'verbose_name': 'Contact form data',
                'verbose_name_plural': 'Contact form data',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactFormItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('form_style', models.CharField(max_length=100, verbose_name='Form', choices=fluentcms_contactform.appsettings.FORM_STYLE_CHOICES)),
                ('email_to', models.EmailField(help_text='The email address where submitted forms should be sent to.', max_length=200, verbose_name='Email to')),
                ('success_message', models.TextField(verbose_name='Thank you message')),
            ],
            options={
                'db_table': 'contentitem_fluentcms_contactform_contactformitem',
                'verbose_name': 'Contact form',
                'verbose_name_plural': 'Contact form',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]

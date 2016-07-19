# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("fluent_contents", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'ContactFormData'
        db.create_table(u'fluentcms_contactform_contactformdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submit_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('internal_note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_archived', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('phone_number', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(default=u'', max_length=200)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'fluentcms_contactform', ['ContactFormData'])

        # Adding model 'ContactFormItem'
        db.create_table(u'contentitem_fluentcms_contactform_contactformitem', (
            (u'contentitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fluent_contents.ContentItem'], unique=True, primary_key=True)),
            ('form_style', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email_to', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('success_message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'fluentcms_contactform', ['ContactFormItem'])

    def backwards(self, orm):
        # Deleting model 'ContactFormData'
        db.delete_table(u'fluentcms_contactform_contactformdata')

        # Deleting model 'ContactFormItem'
        db.delete_table(u'contentitem_fluentcms_contactform_contactformitem')

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fluent_contents.contentitem': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'ContentItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'db_index': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contentitems'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['fluent_contents.Placeholder']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_fluent_contents.contentitem_set+'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'})
        },
        'fluent_contents.placeholder': {
            'Meta': {'unique_together': "(('parent_type', 'parent_id', 'slot'),)", 'object_name': 'Placeholder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'parent_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'slot': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'fluentcms_contactform.contactformdata': {
            'Meta': {'ordering': "(u'submit_date',)", 'object_name': 'ContactFormData'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone_number': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200'}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'fluentcms_contactform.contactformitem': {
            'Meta': {'ordering': "('placeholder', 'sort_order')", 'object_name': 'ContactFormItem', 'db_table': "u'contentitem_fluentcms_contactform_contactformitem'", '_ormbases': ['fluent_contents.ContentItem']},
            u'contentitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fluent_contents.ContentItem']", 'unique': 'True', 'primary_key': 'True'}),
            'email_to': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'form_style': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'success_message': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['fluentcms_contactform']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SmsReceive.parent_sms'
        db.add_column('sms_smsreceive', 'parent_sms', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms.SmsQueue'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SmsReceive.parent_sms'
        db.delete_column('sms_smsreceive', 'parent_sms_id')


    models = {
        'sms.smsqueue': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'SmsQueue'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'flash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sms.SmsSender']", 'null': 'True', 'blank': 'True'}),
            'sms_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'not_sent'", 'max_length': '100', 'blank': 'True'}),
            'test': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'sms.smsreceive': {
            'Meta': {'ordering': "['-date_sent']", 'object_name': 'SmsReceive'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_sms': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sms.SmsQueue']", 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '11'})
        },
        'sms.smssender': {
            'Meta': {'ordering': "['-name']", 'object_name': 'SmsSender'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['sms']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SmsQueue'
        db.create_table('sms_smsqueue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms.SmsSender'], null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('flash', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sms_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='not_sent', max_length=100, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('sms', ['SmsQueue'])

        # Adding model 'SmsReceive'
        db.create_table('sms_smsreceive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('sms', ['SmsReceive'])

        # Adding model 'SmsSender'
        db.create_table('sms_smssender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('sms', ['SmsSender'])


    def backwards(self, orm):
        
        # Deleting model 'SmsQueue'
        db.delete_table('sms_smsqueue')

        # Deleting model 'SmsReceive'
        db.delete_table('sms_smsreceive')

        # Deleting model 'SmsSender'
        db.delete_table('sms_smssender')


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

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'notification'
        db.create_table(u'notification_notification', (
            ('n_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Course'], null=True, blank=True)),
            ('courseName', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sends', to=orm['auth.User'])),
            ('senderName', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tags', to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'notification', ['notification'])

        # Adding model 'activity'
        db.create_table(u'notification_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Course'])),
        ))
        db.send_create_signal(u'notification', ['activity'])

        # Adding model 'message'
        db.create_table(u'notification_message', (
            ('m_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='msends', to=orm['auth.User'])),
            ('senderName', self.gf('django.db.models.fields.CharField')(default='Admin', max_length=256)),
            ('senderImage', self.gf('django.db.models.fields.CharField')(default='fpp/user_blue.png', max_length=256)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mtags', to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'notification', ['message'])


    def backwards(self, orm):
        # Deleting model 'notification'
        db.delete_table(u'notification_notification')

        # Deleting model 'activity'
        db.delete_table(u'notification_activity')

        # Deleting model 'message'
        db.delete_table(u'notification_message')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'notification.activity': {
            'Meta': {'object_name': 'activity'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'notification.message': {
            'Meta': {'object_name': 'message'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'm_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mtags'", 'to': u"orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'msends'", 'to': u"orm['auth.User']"}),
            'senderImage': ('django.db.models.fields.CharField', [], {'default': "'fpp/user_blue.png'", 'max_length': '256'}),
            'senderName': ('django.db.models.fields.CharField', [], {'default': "'Admin'", 'max_length': '256'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'notification.notification': {
            'Meta': {'object_name': 'notification'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.Course']", 'null': 'True', 'blank': 'True'}),
            'courseName': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'n_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tags'", 'to': u"orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sends'", 'to': u"orm['auth.User']"}),
            'senderName': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'student.course': {
            'Meta': {'object_name': 'Course'},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'course_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dept': ('django.db.models.fields.CharField', [], {'default': "'OTHER'", 'max_length': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'There is no description'"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'facultyassociated': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mentor'", 'null': 'True', 'to': u"orm['student.faculty_profile']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'cpp/course_default.png'", 'max_length': '100'}),
            'semester': ('django.db.models.fields.CharField', [], {'default': "'OPEN'", 'max_length': '4'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'student.faculty_profile': {
            'Meta': {'object_name': 'faculty_profile'},
            'areaofinterest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'default': "'CSE'", 'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facultyrating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'fpp/user_blue.png'", 'max_length': '100'}),
            'research': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'weburl': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['notification']
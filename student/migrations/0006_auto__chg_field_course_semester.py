# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Course.semester'
        db.alter_column(u'student_course', 'semester', self.gf('django.db.models.fields.CharField')(max_length=4))

    def backwards(self, orm):

        # Changing field 'Course.semester'
        db.alter_column(u'student_course', 'semester', self.gf('django.db.models.fields.IntegerField')())

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
        u'student.course': {
            'Meta': {'object_name': 'Course'},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'course_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dept': ('django.db.models.fields.CharField', [], {'default': "'OTHER'", 'max_length': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'There is no description'"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'facultyassociated': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mentor'", 'null': 'True', 'to': u"orm['student.faculty_profile']"}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'semester': ('django.db.models.fields.CharField', [], {'default': "'OPEN'", 'max_length': '4'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'student.faculty_profile': {
            'Meta': {'object_name': 'faculty_profile'},
            'areaofinterest': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'facultyrating': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "'/static/uploaded_image/user_blue.png'", 'max_length': '100'}),
            'research': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'weburl': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'student.material': {
            'Meta': {'object_name': 'material'},
            'addedby': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['student.Course']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'There is no Description'"}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'student.student_profile': {
            'Branch': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10'}),
            'DOB': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'student_profile'},
            'Semester': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10'}),
            'coursetaken': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['student.Course']", 'symmetrical': 'False'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['student']
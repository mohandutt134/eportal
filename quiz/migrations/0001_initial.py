# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.TextField()),
                ('a', models.TextField()),
                ('b', models.TextField()),
                ('c', models.TextField()),
                ('d', models.TextField()),
                ('ans', models.CharField(max_length=1, choices=[(b'a', b'option 1'), (b'b', b'option 2'), (b'c', b'option 1'), (b'd', b'option 1')])),
                ('parent', models.ForeignKey(to='student.student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='quiz_spec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('course', models.ForeignKey(to='student.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('course', models.ForeignKey(to='student.Course')),
                ('quiz', models.ForeignKey(to='quiz.quiz_spec')),
                ('user', models.ForeignKey(to='student.student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='quizes',
            field=models.ManyToManyField(to='quiz.quiz_spec'),
            preserve_default=True,
        ),
    ]

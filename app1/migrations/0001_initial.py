# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-17 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clsName', models.CharField(max_length=128, unique=True, verbose_name='班级名称')),
                ('startTime', models.DateField(verbose_name='开课时间')),
                ('endTime', models.DateField(verbose_name='结束时间')),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couName', models.CharField(max_length=64, unique=True, verbose_name='班级名称')),
            ],
        ),
        migrations.CreateModel(
            name='Stu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('phoneNo', models.CharField(max_length=20, verbose_name='手机号')),
                ('qqNo', models.CharField(max_length=15, verbose_name='qq号')),
                ('tuition_total', models.FloatField(verbose_name='应交学费')),
                ('tuition_paid', models.FloatField(verbose_name='已交学费')),
                ('isRecommended', models.BooleanField(verbose_name='是否内部推荐')),
                ('clsType', models.IntegerField(choices=[(1, '现场'), (2, '网络')], default=1, verbose_name='班级类型，1现场，2网络')),
                ('clsId', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='app1.Clas')),
                ('couId', models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.Courses')),
                ('recommender', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.Stu')),
            ],
        ),
        migrations.AddField(
            model_name='clas',
            name='course',
            field=models.ForeignKey(db_constraint=False, default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.Courses'),
        ),
    ]

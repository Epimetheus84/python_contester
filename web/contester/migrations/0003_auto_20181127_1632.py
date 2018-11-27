# Generated by Django 2.1.2 on 2018-11-27 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contester', '0002_auto_20181127_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='input',
            field=models.TextField(verbose_name='Input (separated by semicolon)'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='maximum_time',
            field=models.FloatField(verbose_name='Maximum time of execution'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='output',
            field=models.TextField(verbose_name='Output (separated by semicolon)'),
        ),
    ]

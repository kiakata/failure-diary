# Generated by Django 2.0.5 on 2018-06-06 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nikki', '0006_auto_20180525_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='age',
            new_name='agegroup',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]

# Generated by Django 2.0.5 on 2018-06-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nikki', '0007_auto_20180607_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='agegroup',
            field=models.CharField(max_length=10, verbose_name='年代'),
        ),
    ]

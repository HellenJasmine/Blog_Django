# Generated by Django 5.0.7 on 2024-07-24 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0005_alter_sitesetup_favicon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesetup',
            name='shor_search',
        ),
        migrations.AddField(
            model_name='sitesetup',
            name='show_search',
            field=models.BooleanField(default=True),
        ),
    ]
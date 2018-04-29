# Generated by Django 2.0.3 on 2018-03-30 07:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0010_auto_20180329_1421'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendrequests',
            unique_together={('request_from', 'request_to'), ('request_to', 'request_from')},
        ),
    ]
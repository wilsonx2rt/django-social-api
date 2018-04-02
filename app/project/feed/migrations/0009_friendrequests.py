# Generated by Django 2.0.3 on 2018-03-29 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0008_userprofile_registration_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.CharField(max_length=10, verbose_name='request status')),
                ('request_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to=settings.AUTH_USER_MODEL, verbose_name='sent friend request')),
                ('request_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to=settings.AUTH_USER_MODEL, verbose_name='received friend request')),
            ],
        ),
    ]

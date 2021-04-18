# Generated by Django 3.2 on 2021-04-15 13:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=100)),
                ('post_topic', multiselectfield.db.fields.MultiSelectField(choices=[('P', 'Politics'), ('H', 'Health'), ('T', 'Technology'), ('S', 'Sport')], max_length=7)),
                ('post_created_on', models.DateTimeField(auto_now_add=True)),
                ('post_message', models.TextField()),
                ('post_expiration', models.DateTimeField(default=datetime.datetime(2021, 4, 15, 13, 9, 44, 256793, tzinfo=utc))),
                ('post_status', models.CharField(choices=[('L', 'Live'), ('E', 'Expired')], default='L', max_length=1)),
                ('post_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

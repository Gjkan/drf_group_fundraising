# Generated by Django 4.2.1 on 2024-04-09 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_api', '0008_alter_collect_finish_collect_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collect',
            name='finish_collect_date_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 9, 7, 27, 50, 589959, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения сбора'),
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-28 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrequest',
            name='user_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
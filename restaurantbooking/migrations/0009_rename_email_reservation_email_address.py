# Generated by Django 3.2.18 on 2023-04-30 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantbooking', '0008_auto_20230430_0852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='email',
            new_name='email_address',
       ),
    ]
 
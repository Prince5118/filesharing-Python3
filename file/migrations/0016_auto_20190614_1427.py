# Generated by Django 2.1 on 2019-06-14 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0015_sharedrecord_contenthash'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedrecord',
            name='linkpassword',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='sharedrecord',
            name='linkidentifier',
            field=models.CharField(default='', max_length=255),
        ),
    ]

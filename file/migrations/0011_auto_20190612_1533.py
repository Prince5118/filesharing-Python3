# Generated by Django 2.1 on 2019-06-12 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0010_auto_20190612_1443'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sharedrecord',
            unique_together={('linkidentifier',)},
        ),
    ]

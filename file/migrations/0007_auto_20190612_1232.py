# Generated by Django 2.1 on 2019-06-12 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0006_auto_20190612_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedrecord',
            name='linkidentifier',
            field=models.CharField(default='a', max_length=8),
        ),
        migrations.AlterField(
            model_name='sharedrecord',
            name='contenthash',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='sharedrecord',
            name='pathhash',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='sharedrecord',
            name='reciever',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='sharedrecord',
            unique_together={('contenthash', 'pathhash', 'reciever', 'linkidentifier')},
        ),
    ]

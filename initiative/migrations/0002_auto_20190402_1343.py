# Generated by Django 2.2 on 2019-04-02 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiative', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='is_pc',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='name',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]

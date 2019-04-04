# Generated by Django 2.2 on 2019-04-04 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Initiative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('is_pc', models.BooleanField(default=False)),
                ('initiative', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='initiative.Initiative')),
            ],
        ),
    ]

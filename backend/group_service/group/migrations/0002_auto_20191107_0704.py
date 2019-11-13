# Generated by Django 2.1.14 on 2019-11-07 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191107_0704'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='group',
            name='departure',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='group',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_of_driver', to='user.Driver'),
        ),
        migrations.AddField(
            model_name='group',
            name='from_location',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='group',
            name='to_location',
            field=models.CharField(default='', max_length=255),
        ),
    ]
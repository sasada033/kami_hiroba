# Generated by Django 3.0.4 on 2020-05-25 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khpost', '0003_auto_20200525_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagmodel',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='タグ名'),
        ),
    ]
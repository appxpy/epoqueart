# Generated by Django 4.0.1 on 2022-04-04 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork_status',
            name='artwork_is_available',
            field=models.BooleanField(default=True, help_text='Determines if artwork is available to customers.', verbose_name='Is Available'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='measure',
            field=models.CharField(choices=[('Inch', 'Inch'), ('Millimeter', 'Millimeter')], max_length=24, verbose_name='Measure unit'),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Full name'),
        ),
    ]

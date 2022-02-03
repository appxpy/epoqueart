# Generated by Django 4.0.1 on 2022-01-30 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_painting_name_alter_painting_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='painting',
            name='is_nft',
            field=models.BooleanField(verbose_name='Has NFT?'),
        ),
        migrations.AlterField(
            model_name='painting',
            name='is_offline_available',
            field=models.BooleanField(verbose_name='Available in offline store?'),
        ),
    ]

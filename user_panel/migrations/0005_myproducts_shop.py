# Generated by Django 5.1.4 on 2025-02-11 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0004_alter_myproducts_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='myproducts',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_panel.shop'),
        ),
    ]

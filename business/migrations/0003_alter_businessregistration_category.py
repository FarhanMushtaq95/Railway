# Generated by Django 4.2 on 2023-05-02 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_category_alter_businessregistration_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessregistration',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business_category', to='business.category'),
        ),
    ]

# Generated by Django 5.2.1 on 2025-05-29 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0009_subcategory"),
    ]

    operations = [
        migrations.RenameField(
            model_name="nft",
            old_name="title",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="nft",
            old_name="category",
            new_name="price_irt",
        ),
        migrations.RenameField(
            model_name="nft",
            old_name="price",
            new_name="price_polygon",
        ),
    ]

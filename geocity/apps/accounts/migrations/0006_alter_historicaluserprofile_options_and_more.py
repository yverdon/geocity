# Generated by Django 4.1.4 on 2022-12-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_administrativeentity_sites"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicaluserprofile",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical 3.2 Consultation de l'auteur",
                "verbose_name_plural": "historical 3.2 Consultation des auteurs",
            },
        ),
        migrations.AlterField(
            model_name="historicaluserprofile",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]

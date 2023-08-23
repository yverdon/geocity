# Generated by Django 4.2.1 on 2023-08-03 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0022_contactform_and_more"),
        ("reports", "0030_add_contact_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sectionrecipient",
            name="first_recipient",
            field=models.ForeignKey(
                help_text='Utilisé par défaut. Si celui-ci n\'existe pas, prend le "destinataire secondaire"',
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="first_recipient",
                to="submissions.contacttype",
                verbose_name="Destinataire principal",
            ),
        ),
        migrations.AlterField(
            model_name="sectionrecipient",
            name="second_recipient",
            field=models.ForeignKey(
                help_text='Utilisé lorsque le "destinataire principal" n\'est pas présent dans la liste des contacts saisis',
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="second_recipient",
                to="submissions.contacttype",
                verbose_name="Destinataire secondaire",
            ),
        ),
    ]

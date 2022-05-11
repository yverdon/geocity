# Generated by Django 3.2.12 on 2022-03-29 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0065_permitrequestcomplementarydocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplementaryDocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='nom')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permits.complementarydocumenttype', verbose_name='Type parent')),
                ('work_object_types', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permits.worksobjecttype', verbose_name='Objets')),
            ],
        ),
        migrations.AddConstraint(
            model_name='complementarydocumenttype',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('parent__isnull', False), ('work_object_types__isnull', True)), models.Q(('parent__isnull', True), ('work_object_types__isnull', False)), _connector='OR'), name='Only parent types can be linked to a work object type'),
        ),
    ]
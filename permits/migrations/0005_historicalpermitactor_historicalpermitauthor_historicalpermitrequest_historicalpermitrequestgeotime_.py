# Generated by Django 2.2.13 on 2020-11-08 14:50

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permits', '0004_insert_workflow_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalWorksObjectPropertyValue',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('value', django.contrib.postgres.fields.jsonb.JSONField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.WorksObjectProperty', verbose_name='caractéristique')),
                ('works_object_type_choice', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.WorksObjectTypeChoice', verbose_name='objet des travaux')),
            ],
            options={
                'verbose_name': 'historical works object property value',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPermitRequestValidation',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('validation_status', models.IntegerField(choices=[(0, 'En attente'), (1, 'Approuvé'), (2, 'Refusé')], default=0, verbose_name='Statut de validation')),
                ('comment_before', models.TextField(blank=True, verbose_name='Commentaires (avant)')),
                ('comment_during', models.TextField(blank=True, verbose_name='Commentaires (pendant)')),
                ('comment_after', models.TextField(blank=True, verbose_name='Commentaires (après)')),
                ('validated_at', models.DateTimeField(null=True, verbose_name='Validé le')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('department', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.PermitDepartment')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('permit_request', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.PermitRequest')),
                ('validated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical 3.5 Consultation de la validation par le service',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPermitRequestGeoTime',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('starts_at', models.DateTimeField(verbose_name='Date planifiée de début')),
                ('ends_at', models.DateTimeField(verbose_name='Date planifiée de fin')),
                ('comment', models.CharField(blank=True, max_length=1024, verbose_name='Commentaire')),
                ('external_link', models.URLField(blank=True, verbose_name='Lien externe')),
                ('geom', django.contrib.gis.db.models.fields.GeometryCollectionField(null=True, srid=2056, verbose_name='Localisation')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('permit_request', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.PermitRequest')),
            ],
            options={
                'verbose_name': "historical 3.3 Consultation de l'agenda et de la géométrie",
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPermitRequest',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Brouillon'), (1, 'Envoyée, en attente de traitement'), (4, 'Demande de compléments'), (3, 'En traitement'), (5, 'En validation'), (2, 'Approuvée'), (6, 'Refusée'), (7, 'Annonce réceptionnée')], default=0, verbose_name='état')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date de création')),
                ('validated_at', models.DateTimeField(null=True, verbose_name='date de validation')),
                ('printed_at', models.DateTimeField(null=True, verbose_name="date d'impression")),
                ('printed_by', models.CharField(blank=True, max_length=255, verbose_name='imprimé par')),
                ('printed_file', models.TextField(blank=True, max_length=100, null=True, verbose_name='Permis imprimé')),
                ('archeology_status', models.PositiveSmallIntegerField(choices=[(0, 'Non pertinent'), (1, 'Inconnu'), (2, 'Pas fouillé'), (3, 'Partiellement fouillé'), (4, 'Déjà fouillé')], default=0, verbose_name='Statut archéologique')),
                ('intersected_geometries', models.CharField(max_length=1024, null=True, verbose_name='Entités géométriques concernées')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Émolument')),
                ('exemption', models.TextField(blank=True, verbose_name='Dérogation')),
                ('opposition', models.TextField(blank=True, verbose_name='Opposition')),
                ('comment', models.TextField(blank=True, verbose_name='Analyse du service pilote')),
                ('validation_pdf', models.TextField(max_length=100, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='pdf de validation')),
                ('creditor_type', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Autres'), (2, 'Propriétaire'), (3, 'Entreprise'), (4, "Maître d'ouvrage"), (1, "Requérant si différent de l'auteur de la demande"), (5, 'Sécurité'), (6, 'Association')], null=True, verbose_name='Destinaire de la facture')),
                ('is_public', models.BooleanField(default=False, verbose_name='Publier')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('administrative_entity', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.PermitAdministrativeEntity', verbose_name='commune')),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='permits.PermitAuthor', verbose_name='auteur')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical 3.1 Consultation de la demande',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPermitAuthor',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100, verbose_name='Raison Sociale')),
                ('vat_number', models.CharField(blank=True, max_length=19, validators=[django.core.validators.RegexValidator(message="Le code d'entreprise doit être de type                          CHE-123.456.789 (TVA)                          et vous pouvez le trouver sur                          le registe fédéral des entreprises                          https://www.uid.admin.ch/search.aspx", regex='^(CHE-)+\\d{3}\\.\\d{3}\\.\\d{3}(\\sTVA)?$')], verbose_name='Numéro TVA')),
                ('address', models.CharField(max_length=100, verbose_name='Rue')),
                ('zipcode', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)], verbose_name='NPA')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('phone_first', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Seuls les chiffres et les espaces sont autorisés.', regex='^(((\\+41)\\s?)|(0))?(\\d{2})\\s?(\\d{3})\\s?(\\d{2})\\s?(\\d{2})$')], verbose_name='Téléphone principal')),
                ('phone_second', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Seuls les chiffres et les espaces sont autorisés.', regex='^(((\\+41)\\s?)|(0))?(\\d{2})\\s?(\\d{3})\\s?(\\d{2})\\s?(\\d{2})$')], verbose_name='Téléphone secondaire')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "historical 3.2 Consultation de l'auteur",
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPermitActor',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=100, verbose_name='Nom')),
                ('company_name', models.CharField(max_length=100, verbose_name='Entreprise')),
                ('vat_number', models.CharField(blank=True, max_length=19, verbose_name='Numéro TVA')),
                ('address', models.CharField(max_length=100, verbose_name='Adresse')),
                ('zipcode', models.PositiveIntegerField(verbose_name='NPA')),
                ('city', models.CharField(max_length=100, verbose_name='Ville')),
                ('phone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Contact',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

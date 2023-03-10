from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.management import BaseCommand
from django.utils.translation import gettext

from geocity.apps.reports.models import Report, ReportLayout, SectionParagraph


class Command(BaseCommand):

    help = gettext("Creates default payment and refund print templates.")

    def _create_payment_report(self, group, layout):
        report = Report(
            name="Payment confirmation",
            layout=layout,
            integrator=group,
            is_visible=False,
        )
        report.save()

        section_paragraph_1 = SectionParagraph(
            order=1,
            report=report,
            title="",
            content="""<p><strong>Client n&deg; :&nbsp;{{request_data.properties.author.user_id}}</strong><br />
Date :&nbsp;{{ transaction_data.creation_date }}<br />
<strong>Ann&eacute;e :&nbsp;{{ transaction_data.creation_date_year }}</strong><br />
Page : 1/1</p>""",
            text_align="right",
            location="right",
        )
        section_paragraph_1.save()

        section_paragraph_2 = SectionParagraph(
            order=2,
            report=report,
            title="",
            content="""<p>&nbsp;</p>

<p>{{request_data.properties.author.first_name}}&nbsp;{{request_data.properties.author.last_name}}<br />
{{request_data.properties.author.address}}<br />
{{request_data.properties.author.zipcode}}&nbsp;{{request_data.properties.author.city}}</p>""",
            text_align="right",
            location="right",
        )
        section_paragraph_2.save()

        section_paragraph_3 = SectionParagraph(
            order=3,
            report=report,
            title="",
            content="""<p><strong>FACTURE N&deg; : GEOCITY-{{request_data.id}}</strong></p>

<p>&nbsp;</p>

<p><br />
Pay&eacute; le {{ transaction_data.creation_date }}</p>
            """,
        )
        section_paragraph_3.save()

        section_paragraph_4 = SectionParagraph(
            order=4,
            report=report,
            title="",
            content="""<table border="1" cellpadding="1" cellspacing="1" style="width:100%">
	<tbody>
		<tr>
			<td><strong>Libell&eacute;</strong></td>
			<td>&nbsp;</td>
			<td style="text-align:right"><strong>Prix CHF TTC</strong></td>
		</tr>
		<tr>
			<td>
			<p>&nbsp;</p>

			<p>{{ transaction_data.line_text }} : {{request_data.properties.submission_submission_price.text}}</p>

			<p>&nbsp;</p>
			</td>
			<td>&nbsp;</td>
			<td style="text-align:right">{{request_data.properties.submission_submission_price.amount}}</td>
		</tr>
		<tr>
			<td><strong>Montant pay&eacute;</strong></td>
			<td>&nbsp;</td>
			<td style="text-align:right"><strong>{{request_data.properties.submission_submission_price.amount}}</strong></td>
		</tr>
	</tbody>
</table>

<p>&nbsp;</p>""",
        )
        section_paragraph_4.save()

    def _create_refund_report(self, group, layout):
        report = Report(
            name="Payment refund",
            layout=layout,
            integrator=group,
            is_visible=False,
        )
        report.save()

        section_paragraph_1 = SectionParagraph(
            order=1,
            report=report,
            title="",
            content="""<p><strong>Client n&deg; :&nbsp;{{request_data.properties.author.user_id}}</strong><br />
Date :&nbsp;{{ transaction_data.creation_date }}<br />
<strong>Ann&eacute;e :&nbsp;{{ transaction_data.creation_date_year }}</strong><br />
Page : 1/1</p>""",
            text_align="right",
            location="right",
        )
        section_paragraph_1.save()

        section_paragraph_2 = SectionParagraph(
            order=2,
            report=report,
            title="",
            content="""<p>&nbsp;</p>

<p>{{request_data.properties.author.first_name}}&nbsp;{{request_data.properties.author.last_name}}<br />
{{request_data.properties.author.address}}<br />
{{request_data.properties.author.zipcode}}&nbsp;{{request_data.properties.author.city}}</p>""",
            text_align="right",
            location="right",
        )
        section_paragraph_2.save()

        section_paragraph_3 = SectionParagraph(
            order=3,
            report=report,
            title="",
            content="""<p><strong>REMBOURSEMENT N&deg; : GEOCITY-{{request_data.id}}</strong></p>

<p>&nbsp;</p>

<p><br />
Pay&eacute; le {{ transaction_data.creation_date }}</p>
            """,
        )
        section_paragraph_3.save()

        section_paragraph_4 = SectionParagraph(
            order=4,
            report=report,
            title="",
            content="""<table border="1" cellpadding="1" cellspacing="1" style="width:100%">
	<tbody>
		<tr>
			<td><strong>Libell&eacute;</strong></td>
			<td>&nbsp;</td>
			<td style="text-align:right"><strong>Prix CHF TTC</strong></td>
		</tr>
		<tr>
			<td>
			<p>&nbsp;</p>

			<p>{{ transaction_data.line_text }} : {{request_data.properties.submission_submission_price.text}}</p>

			<p>&nbsp;</p>
			</td>
			<td>&nbsp;</td>
			<td style="text-align:right">-{{request_data.properties.submission_submission_price.amount}}</td>
		</tr>
		<tr>
			<td><strong>Montant rembours&eacute;</strong></td>
			<td>&nbsp;</td>
			<td style="text-align:right"><strong>-{{request_data.properties.submission_submission_price.amount}}</strong></td>
		</tr>
	</tbody>
</table>

<p>&nbsp;</p>""",
        )
        section_paragraph_4.save()

    def handle(self, *args, **options):
        self.stdout.write("Creates default payment print templates ...")

        group = Group.objects.first()
        # Create report setup
        layout = ReportLayout(
            name="Payment layout",
            margin_top=1,
            margin_right=10,
            margin_bottom=20,
            margin_left=22,
            integrator=group,
        )
        _bg_path = finders.find("reports/report-letter-paper-template.png")
        background_image = open(_bg_path, "rb")
        layout.background.save(
            "report-letter-paper.png", File(background_image), save=True
        )
        layout.save()

        self._create_payment_report(group, layout)
        self._create_refund_report(group, layout)

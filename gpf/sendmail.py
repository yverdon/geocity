import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Mail


def send(permit_link, attachments, permit_path, mail_type, recipients):

    mail = Mail.objects.filter(type=mail_type).first()
    emailcontent = mail.body
    if permit_link != '' and mail_type != 'permit_confirmation':
        emailcontent += '<br>Cliquer ici pour consulter la demande<br><br>'
        emailcontent += '<a href="' + permit_link + '">' + permit_link + '</a>'

    subject, from_email= mail.subject, settings.EMAIL_HOST_USER
    html_content = emailcontent
    if recipients == '':
        recipients = mail.recipients.split(',')

    msg = EmailMultiAlternatives(subject, html_content, from_email, recipients)
    msg.attach_alternative(html_content, "text/html")

    if len(attachments) > 0:
        for file in attachments:
            attachment_path = settings.STATIC_ROOT + '/doc/' + file
            msg.attach_file(attachment_path)

    if permit_path != '':
        msg.attach_file(permit_path)

    msg.send()

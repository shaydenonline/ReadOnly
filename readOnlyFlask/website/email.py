from flask_mail import Message
from .. import FLASKY_MAIL_SUBJECT_PREFIX, FLASKY_MAIL_SENDER
from . import mail
from flask import render_template
def send_email(to, subject, template, **kwargs):
    msg = Message(FLASKY_MAIL_SUBJECT_PREFIX + subject,
                  sender=FLASKY_MAIL_SENDER, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
from flask import render_template, current_app
from threading import Thread
from flask_mail import Message
from . import mail


def send_thr_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, tempalte,  **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUNJECT_PREFIX'] + subject, sender=app.config['MAIL_USERNAME'],
                  recipients=[to, 'little_van@126.com'])
    msg.body = render_template(tempalte + '.txt', **kwargs)
    msg.html = render_template(tempalte + '.html', **kwargs)
    thr_mail = Thread(target=send_thr_mail, args=(app, msg))
    thr_mail.start()
    return thr_mail

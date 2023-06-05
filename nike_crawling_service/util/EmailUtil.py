import os
import smtplib
import logging

from dotenv import load_dotenv
from django.template.loader import render_to_string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from nike_crawling_service.util import Properties


load_dotenv()
logger = logging.getLogger('default')


def send_error_email(recipient, reason):
    if recipient:
        plain = f'Crawling Fail!!!\n\n{reason}'
        html = render_to_string('fail.html', {
            'snkr_url': Properties.snkrUrl, 
            'reason': reason
        })
        
        __send_email('Nike SNKRS Crawling Fail!!', recipient, plain, html)    


def send_success_email(recipients, result):
    if recipients:
        count = len(result)
        draw_count = len(list(filter(lambda x: x['draw'] is True, result)))
        normal_count = count - draw_count
        
        plain = f'Count : Draw {draw_count}, Normal {normal_count}'
        html = render_to_string('success.html', {
            'draw_count': draw_count,
            'normal_count': normal_count,
            'snkr_url': Properties.snkrUrl, 
            'items': result
        })
        
        __send_email('Nike SNKRS Crawling Success!!', recipients, plain, html)    
    

def __send_email(subject, recipients, plain, html):
    email_id = os.environ.get('EMAIL_ID')
    email_password = os.environ.get('EMAIL_PASSWORD')
    email_username = os.environ.get('EMAIL_USERNAME')
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f'{email_username} <{email_id}>'
    msg['To'] = recipients

    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(email_id, email_password)
    smtp_server.sendmail(email_id, recipients.split(','), msg.as_string())
    smtp_server.quit()

    log = [
        'Email send!!', 
        f'# Subject : {msg["Subject"]}',
        f'# From : {msg["From"]}', 
        f'# To : {msg["To"]}'
    ]
    logger.info('\n'.join(log))

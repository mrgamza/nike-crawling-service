import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from nike_crawling_service.util import Properties


__all__ = ['EmailUtil']


class EmailUtil:

    load_dotenv()

    email_id = os.environ.get('EMAIL_ID')
    email_password = os.environ.get('EMAIL_PASSWORD')
    email_username = os.environ.get('EMAIL_USERNAME')

    # noinspection PyMethodMayBeStatic
    def __make_success_plain(self, result):
        count = len(result)
        draw_count = len(list(filter(lambda x: x['draw'] is True, result)))
        normal_count = count - draw_count
        return f'Count : Draw {draw_count}, Normal {normal_count}'

    # noinspection PyMethodMayBeStatic
    def __make_success_html(self, result):
        count = len(result)
        draw_count = len(list(filter(lambda x: x['draw'] is True, result)))
        normal_count = count - draw_count
        lines = []
        for item in result:
            line = [f"<h3>{item['name']}</h3>",
                    f"Price : {item['price']}",
                    f"</br>",
                    f"Date : {item['date']}",
                    f"</br>",
                    f"Draw : {item['draw']}",
                    f"</br>",
                    f"<a href='{item['link']}'>Link로 이동</a>"]
            lines.append("".join(line))

        return f'''
        <html>
            <body>
                <h2>Crawling Success!!!</h2>
                <h4>Count : Draw {draw_count}, Normal {normal_count}
                </br>
                <a href='{Properties.snkrUrl}'>SNKRS로 이동</a>
                </br></br>
                {"</br></br>".join(lines)}
            </body>
        </html>
        '''

    # noinspection PyMethodMayBeStatic
    def send_error_email(self, recipient, reason):
        plain = f'Crawling Fail!!!\n\n{reason}'
        html = f'''
        <html>
            <body>
                <h2>Crawling Fail!!!</h2>
                <a href='{Properties.snkrUrl}'>SNKRS로 이동</a>
                </br></br>
                <h3>Reason</h3>
                <p>{reason}</p>
            </body>
        </html>
        '''
        self.send_email(recipient, plain, html)

    # noinspection PyMethodMayBeStatic
    def send_email_result(self, recipient: str, result: str):
        plain = self.__make_success_plain(result)
        html = self.__make_success_html(result)
        self.send_email(recipient, plain, html)

    # noinspection PyMethodMayBeStatic
    def send_email(self, recipient: str, plain: str, html: str):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Nike SNKRS Crawling'
        msg['From'] = f'{self.email_username} <{self.email_id}>'
        msg['To'] = recipient

        msg.attach(MIMEText(plain, 'plain'))
        msg.attach(MIMEText(html, 'html'))

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(self.email_id, self.email_password)
        smtp_server.sendmail(self.email_id, recipient, msg.as_string())
        smtp_server.quit()

        print('send email')
        print(msg)

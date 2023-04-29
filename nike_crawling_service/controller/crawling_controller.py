import json
import requests
import smtplib
import traceback

from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from nike_crawling_service.util import properties


def get_product(parsing_option, test):
    try:
        request = __get_html(properties.crawlingUrl)
        
        if request is None:
            __send_error_email("Response Error", properties.adminEmail)
        else:
            result = __parse(request, parsing_option)
            if not test:
                success_plain = __make_success_plain(result)
                success_html = __make_success_html(result)
                for recipient in properties.recipients:
                    print(success_plain)
                    __send_email(recipient, success_plain, success_html)
            return json.dumps({'data': result})
    except Exception as e:
        print(traceback.format_exc())
        __send_error_email(traceback.format_exc(), properties.adminEmail)

    return json.dumps({'data': 'Error'})


def __get_html(url):
    headers = {
        'User-Agent': properties.userAgent,
        'Accept-Language': 'ko-KR',
        'Accept': 'text/html'
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp
    
    return None


def __parse(html, parsing_option):
    html_text = html.text
    soup = BeautifulSoup(html_text, 'html.parser')
    section = soup.find('section', class_='upcoming-section bg-white ncss-row prl2-md prl5-lg pb4-md pb6-lg')
    find = section.find_all('div', class_='product-card ncss-row mr0-sm ml0-sm')
    
    result = []
    
    today = datetime.today()
    
    for li in find:
        container = li.find('div', class_='ncss-col-sm-12 full')
        if container is None:
            continue
        
        img = container.find('img', class_='image-component mod-image-component u-full-width')
        print(img)
        
        link = __get_link(container)

        container = container.find('div', class_='d-sm-tc va-sm-m')
        if container is None:
            continue

        same_date_only = parsing_option.find('date') > -1
        same_time_only = parsing_option.find('time') > -1

        date_time = __get_date_time(container)
        
        is_draw = __is_draw(container)
        is_same_date = (not same_date_only) or __is_same_date(today, date_time)
        is_same_time = (not same_time_only) or __is_same_time(today, date_time)
 
        append = is_draw and is_same_date and is_same_time
        if append is False:
            continue

        name = __get_name(container)

        result.append({
            'name': name,
            'link': link,
            'date': date_time
        })

    return result


def __get_link(html):
    link = html.find('a', class_='ncss-col-sm-8 launch-details u-full-height va-sm-t full comingsoon')
    if link is not None and link.attrs['href'] is not None:
        return f'https://www.nike.com{link.attrs["href"]}'


def __get_date_time(html):
    date_text = html.find('div', class_='available-date-component').text
    if date_text is None:
        return None

    date_text = date_text.split(' ')[0: 3]
    date_str = ' '.join(date_text).replace('오전', 'AM').replace('오후', 'PM')
    date_time_obj = datetime.strptime(date_str, '%m/%d %p %I:%M')
    date_time_obj = date_time_obj.replace(year=datetime.now().year)
    return date_time_obj


def __get_name(html):
    if html is not None:
        return html.find('h3', class_='headline-5 mb1-sm fs16-sm').string


def __is_draw(html):
    date_text = html.find('div', class_='available-date-component').text
    return date_text.find('응모') > -1


def __is_same_date(current, target):
    return current.year == target.year and current.month == target.month and current.day == target.day


def __is_same_time(current, target):
    return current.hour == target.hour and current.minute == target.minute


def __make_success_plain(result):
    send_count = len(result)
    return f'Crawling Success!!!\nSend : {send_count}'


def __make_success_html(result):
    lines = []
    
    for item in result:
        name = item['name']
        link = item['link']
        date = item['date']

        inner = ""
        inner += f"<h3>{name}</h3>"
        inner += f"Date : {date}"
        inner += f"</br>"
        inner += f"<a href='{link}'>Link로 이동</a>"
        
        lines.append(inner)
        
    return f'''
    <html>
        <body>
            <h2>Crawling Success!!!</h2>
            <a href='{properties.snkrUrl}'>SNKRS로 이동</a>
            </br></br>
            {"</br></br>".join(lines)}
        </body>
    </html>
    '''


def __send_error_email(reason, recipient):
    plain = 'Crawling Fail!!!'
    html = f'''
    <html>
        <body>
            <h2>Crawling Fail!!!</h2>
            <a href='{properties.snkrUrl}'>SNKRS로 이동</a>
            </br></br>
            <h3>Reason</h3>
            <p>{reason}</p>
        </body>
    </html>
    '''
    __send_email(recipient, plain, html)


def __send_email(recipient, plain, html):
    smtp_email = 'your-email@gmail.com'
    from_email = 'your-email@gmail.com'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Nike SNKRS Crawling'
    msg['From'] = f'Your <{from_email}>'
    msg['To'] = recipient
    
    msg.attach(MIMEText(plain, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(smtp_email, properties.gmailPassword)
    smtp_server.sendmail(from_email, recipient, msg.as_string())
    smtp_server.quit()


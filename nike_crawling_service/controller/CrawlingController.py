import json
import os
import traceback

from dotenv import load_dotenv
from nike_crawling_service.parser.Parser230514 import *
from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from nike_crawling_service.util import JSONUtil
from nike_crawling_service.util.EmailUtil import *


load_dotenv()

admin_email = os.environ.get("ADMIN_ID")
email_util = EmailUtil()


def get_product(year, month, day, time, recipients):
    try:
        request = HTMLUtil.get_html(Properties.crawlingUrl)
        if request is None:
            email_util.send_error_email(admin_email, "Response Error")
        else:
            result = Parser230514().parse(request, year, month, day, time)
            if recipients != '':
                recipients_split = recipients.split(',')
                for recipient in recipients_split:
                    email_util.send_email_result(recipient, result)
            dictionary = {
                'recipients': recipients,
                'date': f'{year}-{month}-{day}',
                'time': time,
                'data': result
            }
            return JSONUtil.make_json(dictionary)
    except (Exception,):
        traceback = traceback.format_exc()
        print(traceback)
        email_util.send_error_email(admin_email, traceback)
    return json.dumps({'data': 'Error'})

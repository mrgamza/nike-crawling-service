import json
import os
import traceback

from dotenv import load_dotenv
from nike_crawling_service.parser.Parser import *
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
            result = Parser().parse(request, year, month, day, time)
            if recipients != '':
                recipients_split = recipients.split(',')
                for recipient in recipients_split:
                    email_util.send_email_result(recipient, result)
            dictionary = {
                'recipients': recipients,
                'date': f'{year}-{month}-{day}',
                'time': time,
                'data': list(map(lambda x: x.__dict__, result))
            }
            return JSONUtil.make_json(dictionary)
    except (Exception,):
        trace = traceback.format_exc()
        print(trace)
        email_util.send_error_email(admin_email, trace)
    return json.dumps({'data': 'Error'})

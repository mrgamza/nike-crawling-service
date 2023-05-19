import json
import os
import traceback

from dotenv import load_dotenv
from nike_crawling_service.parser.Parser230514 import *
from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from nike_crawling_service.util.EmailUtil import EmailUtil

load_dotenv()

admin_email = os.environ.get("ADMIN_ID")
email_util = EmailUtil()


def get_product(parsing_option, recipients):
    try:
        request = HTMLUtil.get_html(Properties.crawlingUrl)
        if request is None:
            email_util.send_error_email(admin_email, "Response Error")
        else:
            result = Parser230514().parse(request, parsing_option)
            if recipients != '':
                recipients_split = recipients.split(',')
                for recipient in recipients_split:
                    email_util.send_email_result(recipient, result)
            return json.dumps({'recipients': recipients,
                               'parsing_option': parsing_option,
                               'data': result},
                              default=str)
    except (Exception,):
        email_util.send_error_email(admin_email, traceback.format_exc())
    return json.dumps({'data': 'Error'})

import os
import traceback

from dotenv import load_dotenv

from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from nike_crawling_service.util import JSONUtil
from nike_crawling_service.util import HTTPUtil
from nike_crawling_service.util import EmailUtil
from nike_crawling_service.parser import Parser


def get_product(year, month, day, time, recipients):
    load_dotenv()
    admin_email = os.environ.get("ADMIN_ID")
    
    try:
        request = HTMLUtil.get_html(Properties.crawlingUrl)
        if request is None:
            EmailUtil.send_error_email(admin_email, "Response Error")
        else:
            result = Parser.parse(request, year, month, day, time)
            data = list(map(lambda x: x.__dict__, result))
            if recipients:
                recipients_split = recipients.split(',')
                for recipient in recipients_split:
                    EmailUtil.send_success_email(recipient, data)
            response = HTTPUtil.make_response('0000', 'success', data)
    except (Exception,):
        trace = traceback.format_exc()
        EmailUtil.send_error_email(admin_email, trace)
        print(trace)
        response = HTTPUtil.make_response('1000', trace, None)
    return JSONUtil.make_json(response)

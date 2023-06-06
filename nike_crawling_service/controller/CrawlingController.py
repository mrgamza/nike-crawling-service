import os
import traceback
import logging

from dotenv import load_dotenv

from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from nike_crawling_service.util import JSONUtil
from nike_crawling_service.util import HTTPUtil
from nike_crawling_service.util import EmailUtil
from nike_crawling_service.parser import Parser

from nike_crawling_service.constant.ErrorCode import ErrorCode


logger = logging.getLogger('default')


def get_product(year, month, day, time, recipients):
    load_dotenv()
    admin_email = os.environ.get("ADMIN_ID")
    
    try:
        snkr_response = HTMLUtil.get_html(Properties.crawlingUrl)
        if snkr_response:
            result = Parser.parse(snkr_response, year, month, day, time)
            data = list(map(lambda x: x.__dict__, result))
            
            EmailUtil.send_success_email(recipients, data)
            response = HTTPUtil.make_response(ErrorCode.SUCCESS.value, 'success', data)
            
            logger.info('Success get product')
        else:
            EmailUtil.send_error_email(admin_email, "Response Error")
            response = HTTPUtil.make_response(ErrorCode.RESPONSE_ERROR.value, 'SNKR site response is none', None)
            
            logger.error('SNKR site response is none')
    except (Exception,):
        trace = traceback.format_exc()
        
        EmailUtil.send_error_email(admin_email, trace)
        response = HTTPUtil.make_response(ErrorCode.KNOWN_ERROR.value, trace, None)
        
        logger.error(trace)
    return JSONUtil.make_json(response)

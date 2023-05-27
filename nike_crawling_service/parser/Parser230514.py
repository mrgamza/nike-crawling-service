import traceback
import json

from bs4 import BeautifulSoup
from nike_crawling_service.util import DateUtil
from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from datetime import datetime, timedelta, timezone

__all__ = ['Parser230514']


class Parser230514:
    def parse(self, html, year, month, day, time):
        timezone_kst = timezone(timedelta(hours=9))
        
        time_int = 0 if time is None else int(time)
        request_datetime_kst = datetime(int(year), int(month), int(day), time_int, 0, 0, 0, tzinfo=timezone_kst)

        html_text = html.text
        container = BeautifulSoup(html_text, 'html.parser').find('div', attrs={'data-qa': 'feed-container'})
        main = container.find('main', attrs={'data-qa': 'upcoming-section'})
        products = main.find_all('figure')

        results = []

        for index, product in enumerate(products):
            try:
                draw_pdp = self.__get_pdp(product)
                if draw_pdp is None:
                    continue
                
                date_time = draw_pdp['datetime']
                
                if date_time is None:
                    date_time = self.__get_datetime_for_list(product)
                    is_time_check = False
                else:
                    is_time_check = True
                    
                draw_pdp['datetime'] = date_time
                    
                is_same_date = DateUtil.is_same_date(request_datetime_kst, date_time)
                if is_same_date is False:
                    continue
                
                if is_time_check is True:
                    is_same_time = True if time is None else \
                        DateUtil.is_same_hour(request_datetime_kst, date_time)
                else:
                    is_same_time = True
                
                if is_same_time is False:
                    continue
                
                print("### Find product", index)
                print(json.dumps(draw_pdp, indent=2, default=str))
                
                results.append(draw_pdp)
            except Exception as exception:
                print("### Error product index", index)
                print(traceback.format_exc())
                raise exception
        return results

    # noinspection PyMethodMayBeStatic
    def __get_pdp(self, product):
        product_card_link = product.find('a', attrs={'data-qa': 'product-card-link'})
        if product_card_link is None:
            return None

        link = Properties.detailPrefixUrl + product_card_link.attrs["href"]
        response = HTMLUtil.get_html(link)
        response_text = response.text
        find = response_text.find('Draw로 출시됩니다')
        is_draw = find != -1
        
        soup = BeautifulSoup(response_text, 'html.parser')
        pdp = soup.find('div', attrs={'class': 'product-info ncss-col-sm-12 full ta-sm-c'})
        if pdp is None:
            pdp = soup.find('div', attrs={'class': 'product-info ncss-col-sm-12 full'})
            name = pdp.find('h1', attrs={'class': 'headline-5 pb3-sm'}).text
            description = pdp.find('h2', attrs={'class': 'headline-1 pb3-sm'}).text
            price = pdp.find('div', attrs={'class': 'headline-5 pb6-sm fs14-sm fs16-md'}).text
        else:
            name = pdp.find('h1', attrs={'class': 'headline-5=small'}).text
            description = pdp.find('h2', attrs={'class': 'headline-2'}).text
            price = pdp.find('div', attrs={'class': 'headline-5 pb6-sm'}).text
            
        date_time_html = pdp.find('div', attrs={'class': 'available-date-component'})
        if date_time_html is None:
            date_time = None
        else:
            date_time = self.__get_datetime_for_pdp(date_time_html.text)
        
        return {
            'name': name,
            'description': description,
            'price': price,
            'link': link,
            'datetime': date_time,
            'draw': is_draw
        }
        
    # noinspection PyMethodMayBeStatic
    def __get_datetime_for_list(self, product):
        if product is None:
            return None

        product_card = product.find('div', attrs={'class': 'product-card ncss-row mr0-sm ml0-sm'})
        date_div = product_card.find('div',  attrs={'class': 'launch-caption ta-sm-c'}, recursive=True)
    
        month = date_div.find('p', attrs={'class': 'headline-4'}).text.replace('월', '')
        day = date_div.find('p', attrs={'class': 'headline-1'}).text.replace('일', '')
        date_time = datetime(datetime.now().year, int(month), int(day))
        
        return date_time
    

    # noinspection PyMethodMayBeStatic
    def __get_datetime_for_pdp(self, date_text):
        if date_text is None:
            return None

        transform_text = date_text.replace("출시", "").split(' ')[0: 3]
        date_str = ' '.join(transform_text).replace('오전', 'AM').replace('오후', 'PM')
        timezone_kst = timezone(timedelta(hours=9))
        date_time_obj = datetime.strptime(date_str, '%m/%d %p %I:%M')
        date_time_obj = date_time_obj.replace(year=datetime.now().year,
                                              hour=(date_time_obj.hour + 9))
        return date_time_obj

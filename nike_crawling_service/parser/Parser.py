import traceback

from bs4 import BeautifulSoup
from nike_crawling_service.util import DateUtil
from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from nike_crawling_service.model import Model
from datetime import datetime
from pytz import timezone, utc


__all__ = ['Parser']


class Parser:
    def parse(self, html, year, month, day, time):
        time_int = int(time) if time else 0
        request_datetime_kst = datetime(int(year), int(month), int(day), time_int, 0, 0, 0, tzinfo=timezone('Asia/Seoul'))
        
        html_text = html.text
        container = BeautifulSoup(html_text, 'html.parser').find('div', attrs={'data-qa': 'feed-container'})
        main = container.find('main', attrs={'data-qa': 'upcoming-section'})
        products = main.find_all('figure')
        length = len(products)

        results = []
        
        is_target_date_start = False

        for index, product in enumerate(products):
            try:
                print(f'### Check product ({index+1}/{length})')
                
                draw_pdp = self.__get_pdp(product)
                if not draw_pdp:
                    continue
                
                draw_pdp, can_time_check = self.__set_datetime_for_list(draw_pdp, product)
                
                date_time = draw_pdp.date_time
                if not date_time:
                    continue
                    
                is_same_date = DateUtil.is_same_date(request_datetime_kst, date_time)
                if is_same_date:
                    is_target_date_start = True
                elif is_target_date_start:
                    break
                else:
                    continue
                
                is_same_time = DateUtil.is_same_hour(request_datetime_kst, date_time) \
                   if time and can_time_check else True
                if not is_same_time:
                    continue
                
                results.append(draw_pdp)
            except Exception as exception:
                print("### Error product index", index)
                print(traceback.format_exc())
                raise exception
        return results

    
    def __set_datetime_for_list(self, pdp, product):
        if not pdp.date_time:
            pdp.date_time = self.__datetime_for_list(product)
            can_time_check = False
        else:
            can_time_check = True
            
        return pdp, can_time_check


    def __get_pdp(self, product):
        product_card_link = product.find('a', attrs={'data-qa': 'product-card-link'})
        if not product_card_link:
            return None

        link = Properties.detailPrefixUrl + product_card_link.attrs["href"]
        response = HTMLUtil.get_html(link)
        response_text = response.text
        find = response_text.find('Draw로 출시됩니다')
        is_draw = find != -1
        
        soup = BeautifulSoup(response_text, 'html.parser')
        pdp = soup.find('div', attrs={'class': 'product-info ncss-col-sm-12 full ta-sm-c'})
        if not pdp:
            pdp = soup.find('div', attrs={'class': 'product-info ncss-col-sm-12 full'})
            name = pdp.find('h1', attrs={'class': 'headline-5 pb3-sm'}).text
            description = pdp.find('h2', attrs={'class': 'headline-1 pb3-sm'}).text
            price = pdp.find('div', attrs={'class': 'headline-5 pb6-sm fs14-sm fs16-md'}).text
        else:
            name = pdp.find('h1', attrs={'class': 'headline-5=small'}).text
            description = pdp.find('h2', attrs={'class': 'headline-2'}).text
            price = pdp.find('div', attrs={'class': 'headline-5 pb6-sm'}).text
            
        date_time_html = pdp.find('div', attrs={'class': 'available-date-component'}, recursive=True)
        date_time = self.__datetime_for_pdp(date_time_html.text) \
            if date_time_html else None
        
        return Model.PDP(name, description, price, link, date_time, is_draw)
    
    
    def __now_year(self):
        return int(datetime.now().year)
    
    
    def __datetime_for_list(self, product):
        if not product:
            return None

        product_card = product.find('div', attrs={'class': 'product-card ncss-row mr0-sm ml0-sm'})
        date_div = product_card.find('div',  attrs={'class': 'launch-caption ta-sm-c'}, recursive=True)
    
        month = date_div.find('p', attrs={'class': 'headline-4'}).text.replace('월', '')
        day = date_div.find('p', attrs={'class': 'headline-1'}).text.replace('일', '')
        date_time = datetime(self.__now_year(), int(month), int(day))
        
        return date_time
    
    
    def __datetime_for_pdp(self, date_text):
        if not date_text:
            return None

        transform_text = date_text.replace("출시", "").split(' ')[0: 3]
        date_str = ' '.join(transform_text).replace('오전', 'AM').replace('오후', 'PM')
        date_time_obj = datetime.strptime(date_str, '%m/%d %p %I:%M')
        hour_kst = date_time_obj.hour + 9
        
        return date_time_obj.replace(year=self.__now_year(), hour=hour_kst)


from bs4 import BeautifulSoup
from nike_crawling_service.util import DateUtil
from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from datetime import datetime, timedelta, timezone

__all__ = ['Parser230514']


class Parser230514:
    def parse(self, html, year, month, day):
        timezone_kst = timezone(timedelta(hours=9))
        request_datetime_kst = datetime(int(year), int(month), int(day), 0, 0, 0, 0, tzinfo=timezone_kst)

        html_text = html.text
        find = BeautifulSoup(html_text, 'html.parser').find('div', attrs={'data-qa': 'feed-container'})
        main = find.find('main', attrs={'data-qa': 'upcoming-section'})
        products = main.find_all('figure')

        results = []

        for product in products:
            draw_pdp = self.__get_draw_pdp(product)

            if draw_pdp is None:
                continue

            is_draw = draw_pdp['draw']

            try:
                soup = BeautifulSoup(draw_pdp['response'], 'html.parser')
                inner = soup.find('div', attrs={'class': 'product-info ncss-col-sm-12 full'})
                name = inner.find('h1', attrs={'class': 'headline-5 pb3-sm'}).text
                description = inner.find('h2', attrs={'class': 'headline-1 pb3-sm'}).text
                price = inner.find('div', attrs={'headline-5 pb6-sm fs14-sm fs16-md'}).text
                date_time_html = inner.find('div', attrs={'available-date-component'})
                date_time = self.__get_datetime(date_time_html.text)
                is_same_date = DateUtil.is_same_date(request_datetime_kst, date_time)

                if is_same_date is False:
                    continue

                results.append({
                    'name': f'{name} - {description}',
                    'link': draw_pdp['link'],
                    'price': price,
                    'date': date_time,
                    "draw": draw_pdp['draw']
                })
            except Exception as exception:
                raise exception
        return results

    # noinspection PyMethodMayBeStatic
    def __get_draw_pdp(self, product):
        product_card_link = product.find('a', attrs={'data-qa': 'product-card-link'})
        if product_card_link is None:
            return None

        link = Properties.detailPrefixUrl + product_card_link.attrs["href"]
        response = HTMLUtil.get_html(link)
        response_text = response.text
        find = response_text.find('Draw로 출시됩니다')
        is_draw = find != -1
        return {
            'response': response_text,
            'link': link,
            'draw': is_draw
        }

    # noinspection PyMethodMayBeStatic
    def __get_datetime(self, date_text):
        if date_text is None:
            return None

        transform_text = date_text.replace("출시", "").split(' ')[0: 3]
        date_str = ' '.join(transform_text).replace('오전', 'AM').replace('오후', 'PM')
        date_time_obj = datetime.strptime(date_str, '%m/%d %p %I:%M')
        date_time_obj = date_time_obj.replace(year=datetime.now().year,
                                              hour=(date_time_obj.hour + 9))
        return date_time_obj

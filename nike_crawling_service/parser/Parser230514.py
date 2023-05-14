from bs4 import BeautifulSoup
from nike_crawling_service.util import HTMLUtil
from nike_crawling_service.util import Properties
from datetime import datetime

__all__ = ['Parser230514']


class Parser230514:
    def parse(self, html, parsing_option):
        same_date_only = parsing_option.find('date') > -1
        same_time_only = parsing_option.find('time') > -1
        today = datetime.today()

        html_text = html.text
        find = BeautifulSoup(html_text, 'html.parser').find('div', attrs={'data-qa': 'feed-container'})
        main = find.find('main', attrs={'data-qa': 'upcoming-section'})
        products = main.find_all('figure')

        results = []

        for product in products:
            draw_pdp = self.__get_draw_pdp(product)
            if draw_pdp is None:
                continue

            try:
                inner = BeautifulSoup(draw_pdp['response'], 'html.parser').find('div', attrs={
                    'class': 'product-info ncss-col-sm-12 full'})
                name = inner.find('h1', attrs={'class': 'headline-5 pb3-sm'}).text
                description = inner.find('h2', attrs={'class': 'headline-1 pb3-sm'}).text
                price = inner.find('div', attrs={'headline-5 pb6-sm fs14-sm fs16-md'}).text
                date_time = inner.find('div', attrs={'available-date-component'})

                is_same_date = (not same_date_only) or self.__is_same_date(today, date_time)
                is_same_time = (not same_time_only) or self.__is_same_time(today, date_time)

                append = is_same_date and is_same_time
                if append is False:
                    continue
                results.append({
                    'name': f'{name} - {description}',
                    'link': draw_pdp['link'],
                    'price': price,
                    'date': self.__get_datetime(date_time.text)
                })
            except Exception as exception:
                print(exception)
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
        if find != -1:
            return {
                'response': response_text,
                'link': link
            }
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def __get_datetime(self, date_text):
        if date_text is None:
            return None

        transform_text = date_text.replace("출시", "").split(' ')[0: 3]
        date_str = ' '.join(transform_text).replace('오전', 'AM').replace('오후', 'PM')
        date_time_obj = datetime.strptime(date_str, '%m/%d %p %I:%M')
        date_time_obj = date_time_obj.replace(year=datetime.now().year)
        return date_time_obj

    # noinspection PyMethodMayBeStatic
    def __is_same_date(self, current, target):
        return current.year == target.year and current.month == target.month and current.day == target.day

    # noinspection PyMethodMayBeStatic
    def __is_same_time(self, current, target):
        return current.hour == target.hour and current.minute == target.minute

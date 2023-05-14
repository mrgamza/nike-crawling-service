from bs4 import BeautifulSoup
from datetime import datetime


__all__ = ['Parser']


class Parser:
    def parse(self, html, parsing_option):
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

            link = self.__get_link(container)

            container = container.find('div', class_='d-sm-tc va-sm-m')
            if container is None:
                continue

            same_date_only = parsing_option.find('date') > -1
            same_time_only = parsing_option.find('time') > -1

            date_time = self.__get_date_time(container)

            is_draw = self.__is_draw(container)
            is_same_date = (not same_date_only) or self.__is_same_date(today, date_time)
            is_same_time = (not same_time_only) or self.__is_same_time(today, date_time)

            append = is_draw and is_same_date and is_same_time
            if append is False:
                continue

            name = self.__get_name(container)

            result.append({
                'name': name,
                'link': link,
                'date': date_time
            })

        return result

    # noinspection PyMethodMayBeStatic
    def __get_link(self, html):
        link = html.find('a', class_='ncss-col-sm-8 launch-details u-full-height va-sm-t full comingsoon')
        if link is not None and link.attrs['href'] is not None:
            return f'https://www.nike.com{link.attrs["href"]}'

    # noinspection PyMethodMayBeStatic
    def __get_date_time(self, html):
        date_text = html.find('div', class_='available-date-component').text
        if date_text is None:
            return None

        date_text = date_text.split(' ')[0: 3]
        date_str = ' '.join(date_text).replace('오전', 'AM').replace('오후', 'PM')
        date_time_obj = datetime.strptime(date_str, '%m/%d %p %I:%M')
        date_time_obj = date_time_obj.replace(year=datetime.now().year)
        return date_time_obj

    # noinspection PyMethodMayBeStatic
    def __get_name(self, html):
        if html is not None:
            return html.find('h3', class_='headline-5 mb1-sm fs16-sm').string

    # noinspection PyMethodMayBeStatic
    def __is_draw(self, html):
        date_text = html.find('div', class_='available-date-component').text
        return date_text.find('응모') > -1

    # noinspection PyMethodMayBeStatic
    def __is_same_date(self, current, target):
        return current.year == target.year and current.month == target.month and current.day == target.day

    # noinspection PyMethodMayBeStatic
    def __is_same_time(self, current, target):
        return current.hour == target.hour and current.minute == target.minute

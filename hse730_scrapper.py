import sys
import pandas as pd
from bs4 import BeautifulSoup
from property_setting import DATA_PATH, NOTIFIER_PATH, NETDATA_PATH, IO_PATH, Hse730Setting
from chat_id import CHAT_ID
sys.path.append(NETDATA_PATH)
sys.path.append(NOTIFIER_PATH)
sys.path.append(IO_PATH)
from web_scrapper import WebScrapper
from telegram_notifier import TelegramNotifier
from file_io import FileIO
from netdata_utilities import check_html_element_exist


class Hse730(Hse730Setting):

    def __init__(self):
        self.scrapper = WebScrapper()
        self.io = FileIO()
        self.notifier = TelegramNotifier()

    def _search_result_checker(self, html):
        return check_html_element_exist(html, self.RESULT_TAG)

    def _property_page_checker(self, html):
        return check_html_element_exist(html, self.PROPERTY_TAB)

    def get_check_id(self):
        sent_id = self.io.load_file(DATA_PATH, self.CHECK_ID_FILE, 'json')
        return sent_id

    def get_search_url_list(self):
        url_list = [self.RESULT_URL.format(''.join(self.DISTRICT), page_no + 1, self.LOWEST_PRICE, self.HIGHEST_PRICE)
                    for page_no in range(self.CHECK_NO_PAGE)]
        return url_list

    def get_html_result_pages(self, url_list):
        response_list = self.scrapper.load_multiple_html(
            url_list, html_checker=self._search_result_checker, asyn=True)
        return response_list

    @staticmethod
    def _get_property_id_from_url(url):
        if '/buy-property-' not in url:
            property_id = -1
        else:
            property_id = int(url.replace('https://www.house730.com', '').replace('/buy-property-', '').replace(
                '.html', ''))
        return property_id

    def save_check_id(self, new_check_id_list):
        self.io.save_file(new_check_id_list, DATA_PATH, self.CHECK_ID_FILE, 'json')

    def get_property_url_from_html(self, response, check_id):
        if response['ok']:
            soup = BeautifulSoup(response['message'], 'html.parser')
            result_list = soup.select(self.RESULT_TAG)[0]
            property_url_list = [property_tag.get('href') for property_tag in result_list.select('a.name')]
            property_url_list = ['https://www.house730.com' + property_url for property_url in property_url_list
                                 if self._get_property_id_from_url(property_url) not in check_id]
            return property_url_list
        else:
            self.notifier.send_message('Unable to load result for page {}. {}'.format(
                response['url'], response['error']))
            return []

    def aggregate_property_url(self, response_list, check_id):
        property_url_list = list(map(
            lambda response: self.get_property_url_from_html(response, check_id), response_list))
        property_url_list = [url for property_url in property_url_list for url in property_url]
        return property_url_list

    def append_new_check_id_list(self, property_url_list, check_id):
        new_check_id_list = [self._get_property_id_from_url(property_url) for property_url in property_url_list]
        new_check_id_list += check_id
        new_check_id_list = new_check_id_list[:50]
        self.save_check_id(new_check_id_list)

    def get_property_pages(self, property_url_list):
        response_list = self.scrapper.load_multiple_html(property_url_list, html_checker=self._property_page_checker)
        return response_list

    def extract_property_pages(self, response):
        if response['ok']:
            soup = BeautifulSoup(response['message'], 'html.parser')
            property_table = pd.read_html(str(soup.select(self.PROPERTY_TAB)[0]))[0]
            property_table = property_table.set_index(0).T
            property_table = property_table.assign(**{'URL': response['url']})
            return property_table
        else:
            self.notifier.send_message('Unable to load property for page {}. {}'.format(response['url'],
                                                                                        response['error']))
            return pd.DataFrame([])

    def aggregate_property_table(self, response_list):
        property_data_list = list(map(self.extract_property_pages, response_list))
        if len(property_data_list) > 0:
            property_data = pd.concat(property_data_list, sort=False)
            property_data = property_data.set_index('House730樓盤編號')
        else:
            property_data = pd.DataFrame([])
        return property_data

    def clean_filter_property_table(self, property_data):
        property_data = property_data.assign(**{
            '售價': property_data.loc[:, '售價'].str.split('按揭計算機').str[0],
            '樓盤地址': property_data.loc[:, '樓盤地址'].str.replace('屋苑位置', '')
        })
        property_data = property_data.loc[
            (property_data.loc[:, '實用面積(呎)'].str.replace('[^0-9]', '').astype(float) >= self.SMALLEST_SIZE) |
            (property_data.loc[:, '實用面積(呎)'].isnull())]
        property_data = property_data.loc[
            (property_data.loc[:, '樓齡(年)'].str.replace('[^0-9]', '').astype(float) <= self.OLDEST_PROPERTY) |
            (property_data.loc[:, '樓齡(年)'].isnull())]
        property_data = property_data.loc[~property_data.loc[:, '售價'].str.contains('居屋')]
        property_data = property_data.drop(
            ['物業編號', '樓盤狀態', '瀏覽人次', '刊登或續期日', '記錄更新', '放盤到期日'], axis=1)
        property_data = property_data.fillna('')
        return property_data

    @staticmethod
    def convert_property_dict_to_str(property_dict):
        message_str = ''
        for key, value in property_dict.items():
            message_str += '{}: {}\n'.format(key, value)
        return message_str

    def send_property_details(self, property_data):
        property_records = property_data.to_dict('records')
        message_list = list(map(self.convert_property_dict_to_str, property_records))
        for chat_id in CHAT_ID:
            self.notifier.CHAT_ID = chat_id
            list(map(self.notifier.send_message, message_list))

    def hse730_scrapping(self):
        check_id = self.get_check_id()
        url_list = self.get_search_url_list()
        response_list = self.get_html_result_pages(url_list)
        property_url_list = self.aggregate_property_url(response_list, check_id)
        self.append_new_check_id_list(property_url_list, check_id)
        response_list = self.get_property_pages(property_url_list)
        property_data = self.aggregate_property_table(response_list)
        if len(property_data) > 0:
            property_data = self.clean_filter_property_table(property_data)
        if len(property_data) > 0:
            self.send_property_details(property_data)


if __name__ == '__main__':
    hse730 = Hse730()
    hse730.hse730_scrapping()
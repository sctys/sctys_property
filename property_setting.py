DATA_PATH = '/media/sctys/Seagate Expansion Drive/Data/sctys_property'
NETDATA_PATH = '/media/sctys/Seagate Expansion Drive/Projects/sctys_netdata'
NOTIFIER_PATH = '/media/sctys/Seagate Expansion Drive/Projects/sctys_notify'
IO_PATH = '/media/sctys/Seagate Expansion Drive/Projects/sctys_io'
MODE = 'thread'


class Hse28Setting(object):
    RESULT_URL = 'https://www.28hse.com/buy/district-g{}/house-type-g1'
    DISTRICT = ['g4', 'g5', 'g6', 'g7', 'g8', 'g9']
    TEMP_ID_FILE = 'latest_id.json'
    RESULT_TAG = 'div#search_result_div'
    LOAD_TAG = 'div#search_main_div.agentad_outer'
    FILTER_TAG = 'dl.sales_price a[data-bind="4"]'
    LOW_PRICE_TAG = 'input#rentpriceTxtS.sh-text.low'
    HIGH_PRICE_TAG = 'input#rentpriceTxtE.sh-text.high'
    PRICE_BUTTON_TAG = 'span.text-search-btn'
    SORT_TAG = 'div.search_ranking a[data-inside="1"]'
    PROPERTY_TAB = 'table.de_box_table'
    OLDEST_PROPERTY = 45
    SMALLEST_SIZE = 350
    LOWEST_PRICE = '600'
    HIGHEST_PRICE = '830'


class Hse730Setting(object):
    RESULT_URL = 'https://www.house730.com/buy/{}t1u14g{}/?pmin={}&pmax={}' # district string, page no, min price, max price
    DISTRICT = ['hma076', 'hma160', 'hma144', 'hma032', 'hma014', 'hma130', 'hma126', 'hmab01', 'hma041', 'hma110',
                'hma034', 'hma113']
    CHECK_NO_PAGE = 2
    CHECK_ID_FILE = 'check_id.json'
    RESULT_TAG = 'div.house-lists.clearfix'
    PROPERTY_TAB = 'table.baseinfor'
    OLDEST_PROPERTY = 45
    SMALLEST_SIZE = 350
    LOWEST_PRICE = '600'
    HIGHEST_PRICE = '830'


DATA_PATH = '/media/sctys/Seagate Expansion Drive/Data/sctys_property'
NETDATA_PATH = '/media/sctys/Seagate Expansion Drive/Projects/sctys_netdata'
NOTIFIER_PATH = '/media/sctys/Seagate Expansion Drive/Projects/sctys_notify'
IO_PATH = '/media/sctys/Seagate Expansion Drive/Projects/sctys_io'
NOTIFIER = 'telegram'
MODE = 'thread'


class Hse28Setting(object):
    RESULT_URL = 'https://www.28hse.com/buy/district-g{}/house-type-g1'
    DISTRICT = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9', 'g10']
    TEMP_ID_FILE = 'latest_id.json'
    RESULT_TAG = 'div#search_result_div'
    LOAD_TAG = 'div#search_main_div.agentad_outer'
    FILTER_TAG = 'dl.sales_price a[data-bind="4"]'
    SORT_TAG = 'div.search_ranking a[data-inside="1"]'
    PROPERTY_TAB = 'table.de_box_table'
    OLDEST_PROPERTY = 45
    SMALLEST_SIZE = 300



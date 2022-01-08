import unittest
import datetime
from time import sleep 

from portfolio.classes.securities import Security

class TestInit(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_var(self):
        self.stock = Security('SE0012673267')
        self.fund = Security('SE0012193019')
        self.currency_cross = Security('USD/SEK')

    def test_type(self):
        self.assertRaises(TypeError, Security, None)
        self.assertRaises(TypeError, Security, 1)
        self.assertRaises(TypeError, Security, 1.0)
        self.assertRaises(TypeError, Security, list())
        self.assertRaises(TypeError, Security, 5j)
        self.assertRaises(TypeError, Security, 1)
        self.assertRaises(TypeError, Security, 1)
        self.assertRaises(TypeError, Security, 1)

    def test_create_var_unproparly(self):
        self.assertRaises(ValueError, Security, '')
        self.assertRaises(RuntimeError, Security, 'xxxxxxxxxx')
        self.assertRaises(RuntimeError, Security, 'USD/xxx') 
        self.assertRaises(RuntimeError, Security, 'abc')
        self.assertRaises(RuntimeError, Security, '123')

class TestMethod_get_search_security_query_investpy(unittest.TestCase):
    def setUp(self):
        self.security = Security('SE0012673267')
        self.expected_outputs = {
            1: 'investpy.search_stocks(by= "isin", value= \"SE0012673267\")',
            2: 'investpy.search_funds(by= "isin", value= \"SE0012193019\")',
            3: 'investpy.search_currency_crosses(by= "name", value= \"USD/SEK\")',
            }
        self.from_date = datetime.date(year=2021, month=1,  day=1)
        self.to_date   = datetime.date(year=2021, month=12, day=31)

    def test_type_error_raise(self):
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, None,   'SE0012673267')
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 1,      'SE0012673267')
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, list(), 'SE0012673267')
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, -1.0,   'SE0012673267')
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 5j,     'SE0012673267')

        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 'stock',   None)
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 'stock',      1)
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 'stock', list())
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 'stock',   -1.0)
        self.assertRaises(TypeError, self.security.get_search_security_query_investpy, 'stock',     5j)

    def test_value_error_raise(self):
        self.assertRaises(ValueError, self.security.get_search_security_query_investpy, 'abc',   'SE0012673267')

    def test_output(self):
        self.assertEqual(self.security.get_search_security_query_investpy('stock', 'se0012673267'), self.expected_outputs[1])
        self.assertEqual(self.security.get_search_security_query_investpy('Stock', 'Se0012673267'), self.expected_outputs[1])
        self.assertEqual(self.security.get_search_security_query_investpy('STOCK', 'sE0012673267'), self.expected_outputs[1])
        self.assertEqual(self.security.get_search_security_query_investpy('sTock', 'SE0012673267'), self.expected_outputs[1])

        self.assertEqual(self.security.get_search_security_query_investpy('fund', 'se0012193019'), self.expected_outputs[2])
        self.assertEqual(self.security.get_search_security_query_investpy('Fund', 'Se0012193019'), self.expected_outputs[2])
        self.assertEqual(self.security.get_search_security_query_investpy('FUND', 'sE0012193019'), self.expected_outputs[2])
        self.assertEqual(self.security.get_search_security_query_investpy('funD', 'SE0012193019'), self.expected_outputs[2])

        self.assertEqual(self.security.get_search_security_query_investpy('Currency_cross', 'usd/SEK'), self.expected_outputs[3])
        self.assertEqual(self.security.get_search_security_query_investpy('currency_Cross', 'USD/sek'), self.expected_outputs[3])
        self.assertEqual(self.security.get_search_security_query_investpy('CURRENCY_CROSS', 'usd/sek'), self.expected_outputs[3])
        self.assertEqual(self.security.get_search_security_query_investpy('currency_cross', 'USD/SEK'), self.expected_outputs[3])

class TestMethod_get_basic_info(unittest.TestCase):
    def setUp(self):
        # test stock function on Evolution Gaming Group AB
        self.stock_data = {
            'name'          : 'Evolution Gaming',
            'full_name'     : 'Evolution Gaming Group AB',
            'security_type' : 'stock',
            'isin'          : 'SE0012673267',
            'symbol'        : 'EVOG',
            'country'       : 'sweden',
            'currency'      : 'SEK'
        }  
        # test fund function on TIN NyTeknik 
        self.fund_data = {
            'name'          : 'Core Ny Teknik A',
            'full_name'     :  None,
            'security_type' : 'fund',
            'isin'          : 'SE0012193019',
            'symbol'        : '0P0001FLH9',
            'country'       : 'sweden',
            'currency'      : 'SEK'
        }
        # test currency cross on USD/SEK
        self.currency_cross_data = {
            'name'          : 'USD/SEK',
            'full_name'     : 'USD/SEK - US Dollar Swedish Krona',
            'security_type' : 'currency_cross',
            'isin'          :  None,
            'symbol'        :  None,
            'country'       :  None,
            'currency'      : 'SEK'
        }
        self.stock = Security(self.stock_data['isin'])
        self.fund = Security(self.fund_data['isin'])
        self.currency_cross = Security(self.currency_cross_data['name'])

    def test_output_type(self):
        self.assertEqual(type(self.stock.get_basic_info())          , dict)
        self.assertEqual(type(self.fund.get_basic_info())           , dict)
        self.assertEqual(type(self.currency_cross.get_basic_info()) , dict)

    def test_output_for_stock(self):
        results_stock = self.stock.get_basic_info()

        self.assertEqual(results_stock['name']          , self.stock_data['name'])
        self.assertEqual(results_stock['full_name']     , self.stock_data['full_name'])
        self.assertEqual(results_stock['security_type'] , self.stock_data['security_type'])
        self.assertEqual(results_stock['isin']          , self.stock_data['isin'])
        self.assertEqual(results_stock['symbol']        , self.stock_data['symbol'])
        self.assertEqual(results_stock['country']       , self.stock_data['country'])
        self.assertEqual(results_stock['currency']      , self.stock_data['currency'])


    def test_output_for_fund(self):
        results_fund = self.fund.get_basic_info()

        self.assertEqual(results_fund['name']          , self.fund_data['name'])
        self.assertEqual(results_fund['full_name']     , self.fund_data['full_name'])
        self.assertEqual(results_fund['security_type'] , self.fund_data['security_type'])
        self.assertEqual(results_fund['isin']          , self.fund_data['isin'])
        self.assertEqual(results_fund['symbol']        , self.fund_data['symbol'])
        self.assertEqual(results_fund['country']       , self.fund_data['country'])
        self.assertEqual(results_fund['currency']      , self.fund_data['currency'])

    def test_output_for_currency_cross(self):
        results_currency_cross = self.currency_cross.get_basic_info()

        self.assertEqual(results_currency_cross['name']          , self.currency_cross_data['name'])
        self.assertEqual(results_currency_cross['full_name']     , self.currency_cross_data['full_name'])
        self.assertEqual(results_currency_cross['security_type'] , self.currency_cross_data['security_type'])
        self.assertEqual(results_currency_cross['isin']          , self.currency_cross_data['isin'])
        self.assertEqual(results_currency_cross['symbol']        , self.currency_cross_data['symbol'])
        self.assertEqual(results_currency_cross['country']       , self.currency_cross_data['country'])
        self.assertEqual(results_currency_cross['currency']      , self.currency_cross_data['currency'])


class TestMethod_get_historical_data_query_investpy(unittest.TestCase):
    def setUp(self):
        self.security = Security('SE0012673267')
        self.expected_outputs = {
            1: 'investpy.get_stock_historical_data(\"EVOG\", country= \"sweden\", from_date= \"1/1/2021\", to_date= \"31/12/2021\")',
            2: 'investpy.get_fund_historical_data(\"CORE NY TEKNIK A\", country= \"sweden\", from_date= \"1/1/2021\", to_date= \"31/12/2021\")',
            3: 'investpy.get_currency_cross_historical_data(\"USD/SEK\", from_date= \"1/1/2021\", to_date= \"31/12/2021\")'
        }
        self.from_date = datetime.date(year=2021, month=1,  day=1)
        self.to_date   = datetime.date(year=2021, month=12, day=31)

    def test_type_error_raise(self):
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, None,    'EVOG', 'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 1,       'EVOG', 'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, list(),  'EVOG', 'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, -1.0,    'EVOG', 'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 5j,      'EVOG', 'sweden', self.from_date, self.to_date)

        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', None,   'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 1,      'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', list(), 'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', -1.0,   'sweden', self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 5j,     'sweden', self.from_date, self.to_date)

        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 1,        self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', list(),   self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', -1.0,     self.from_date, self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 5j,       self.from_date, self.to_date)

        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', 'abc',          self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', 1,              self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', list(),         self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', -1.0,           self.to_date)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', 5j,             self.to_date)

        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', self.from_date, 'abc')
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', self.from_date, 1)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', self.from_date, list())
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', self.from_date, -1.0)
        self.assertRaises(TypeError, self.security.get_historical_data_query_investpy, 'stock', 'EVOG', 'sweden', self.from_date, 5j)

        

    def test_value_error_raise(self):
        self.assertRaises(ValueError, self.security.get_historical_data_query_investpy, 'abc',  'EVOG', 'sweden', self.from_date, self.to_date)
    
    def test_output(self):
        self.assertEqual(self.security.get_historical_data_query_investpy('stock',          'EVOG',                 'sweden',   self.from_date, self.to_date), self.expected_outputs[1])
        self.assertEqual(self.security.get_historical_data_query_investpy('fund',           'Core Ny Teknik A',     'sweden',   self.from_date, self.to_date), self.expected_outputs[2])
        self.assertEqual(self.security.get_historical_data_query_investpy('currency_cross', 'USD/SEK',              None,       self.from_date, self.to_date), self.expected_outputs[3])


class TestMethod_get_security_price(unittest.TestCase):
    def setUp(self):
        self.from_date = datetime.date(year=2021, month=1, day=1)
        self.to_date = datetime.date(year=2021, month=1, day=5)

        self.securties = [
            Security('SE0012673267'),
            Security('SE0012193019'),
            Security('USD/SEK')
        ]
        
        self.random_security_prices = {
            'Evolution Gaming': {
                datetime.date(year=2018, month=6,  day=8):  113.0,
                # datetime.date(year=2020, month=2,  day=24): 407.0,
                # datetime.date(year=2020, month=10, day=27): 690.0,
                # datetime.date(year=2021, month=4,  day=29): 1666.2,
                datetime.date(year=2021, month=12,  day=3): 935.0
            },
            'Core Ny Teknik A': {
                datetime.date(year=2020, month=2,  day=24): 140.930,
                # datetime.date(year=2020, month=10, day=27): 187.614,
                # datetime.date(year=2021, month=4,  day=29): 236.883,
                datetime.date(year=2021, month=12,  day=3): 219.191
            },
            'USD/SEK': {
                datetime.date(year=2018, month=6,  day=8):  8.7081,
                # datetime.date(year=2020, month=2,  day=24): 9.7319,
                # datetime.date(year=2020, month=10, day=27): 8.7226,
                # datetime.date(year=2021, month=4,  day=29): 8.3705,
                datetime.date(year=2021, month=12,  day=3): 9.1364
            }
            
        }
        self.security_price_range_short = {
            'Evolution Gaming': {
                datetime.date(year=2022, month=1, day=3): 1282.8,
                datetime.date(year=2022, month=1, day=4): 1282.0,
                datetime.date(year=2022, month=1, day=5): 1284.8
            },
            'Core Ny Teknik A': {
                datetime.date(year=2022, month=1, day=3): 233.817,
                datetime.date(year=2022, month=1, day=4): 231.458,
                datetime.date(year=2022, month=1, day=5): 229.064
            },
            'USD/SEK': {
                datetime.date(year=2022, month=1, day=3): 9.1033,
                datetime.date(year=2022, month=1, day=4): 9.0871,
                datetime.date(year=2022, month=1, day=5): 9.1041
            }
        }
        self.security_price_range_long = {
            'Evolution Gaming': {
                datetime.date(year=2022, month=1, day=1): 1286.2,
                datetime.date(year=2022, month=1, day=2): 1286.2,
                datetime.date(year=2022, month=1, day=3): 1282.8,
                datetime.date(year=2022, month=1, day=4): 1280.0,
                datetime.date(year=2022, month=1, day=5): 1284.8
            },
            'Core Ny Teknik A': {
                datetime.date(year=2022, month=1, day=1): 233.817,
                datetime.date(year=2022, month=1, day=2): 233.817,
                datetime.date(year=2022, month=1, day=3): 233.817,
                datetime.date(year=2022, month=1, day=4): 231.458,
                datetime.date(year=2022, month=1, day=5): 229.064
            },
            'USD/SEK': {
                datetime.date(year=2022, month=1, day=1): 9.0392,
                datetime.date(year=2022, month=1, day=2): 9.0392,
                datetime.date(year=2022, month=1, day=3): 9.1033,
                datetime.date(year=2022, month=1, day=4): 9.0871,
                datetime.date(year=2022, month=1, day=5): 9.1041
            }   
        }

    def test_type(self):
        self.assertRaises(TypeError, self.securties[0].get_security_price(), None,      datetime.date(year=2021, month=5, day=5))
        self.assertRaises(TypeError, self.securties[0].get_security_price(), 'abc',     datetime.date(year=2021, month=5, day=5))
        self.assertRaises(TypeError, self.securties[0].get_security_price(), 1,         datetime.date(year=2021, month=5, day=5))
        self.assertRaises(TypeError, self.securties[0].get_security_price(), list(),    datetime.date(year=2021, month=5, day=5))

        self.assertRaises(TypeError, self.securties[0].get_security_price(), datetime.date(year=2021, month=5, day=5), None)
        self.assertRaises(TypeError, self.securties[0].get_security_price(), datetime.date(year=2021, month=5, day=5), 'abc')
        self.assertRaises(TypeError, self.securties[0].get_security_price(), datetime.date(year=2021, month=5, day=5), 1)
        self.assertRaises(TypeError, self.securties[0].get_security_price(), datetime.date(year=2021, month=5, day=5), list())


    def test_get_security_price_output(self):
        msg = '{security}s stock price don\'t match at date {date}'

        for security in self.securties:
            for date in list(self.random_security_prices[security.get_basic_info()['name']].keys()):
                # Time delay to avoid error code 429 
                # by breaching query limit of investing.com and being blacklisted for 24h
                # https://github.com/alvarobartt/investpy/issues/467
                sleep(5)

                # test whether output is of length 1, i.e. stock price for a given day
                self.assertEqual(len(list(security.get_security_price(date).keys())), 1, msg='output is not for single day')

                # test whether stock price matches raw data
                self.assertEqual(
                    security.get_security_price(date)[date], 
                    self.random_security_prices[security.get_basic_info()['name']][date], 
                    msg=msg.format(security= security.get_basic_info()['name'], date= date)
                )

        

    def test_get_security_historical_price_output(self):
        msg = '{security}s stock price don\'t match at date {date}'

        for security in self.securties:
            for date in list(self.security_price_range_short[security.get_basic_info()['name']].keys()):
                # Time delay to avoid error code 429 
                # by breaching query limit of investing.com and being blacklisted for 24h
                # https://github.com/alvarobartt/investpy/issues/467
                sleep(5)

                # test whether stock price matches raw data
                self.assertEqual(
                    security.get_security_price(date)[date], 
                    self.security_price_range_short[security.get_basic_info()['name']][date], 
                    msg=msg.format(security= security.get_basic_info()['name'], date= date)
                )

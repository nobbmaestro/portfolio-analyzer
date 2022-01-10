import unittest
import datetime
from time import sleep 

from portfolio.classes.security import Security

class TestInit(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_var(self):

        # Time delay to avoid error code 429 from investpy
        # by breaching query limit of investing.com and being blacklisted for 24h
        # https://github.com/alvarobartt/investpy/issues/467

        self.stock = Security('SE0012673267')
        sleep(5)
        self.fund = Security('SE0012193019')
        sleep(5)
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
        self.assertRaises(TypeError, Security, None, None)

    def test_create_var_unproparly(self):
        self.assertRaises(ValueError, Security, '')
        self.assertRaises(RuntimeError, Security, 'xxxxxxxxxx')
        self.assertRaises(RuntimeError, Security, 'USD/xxx') 
        self.assertRaises(RuntimeError, Security, 'abc')
        self.assertRaises(RuntimeError, Security, '123')
        self.assertRaises(ValueError, Security, None, datetime.date.today()+datetime.timedelta(days=1))

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

        # Time delay to avoid error code 429 
        # by breaching query limit of investing.com and being blacklisted for 24h
        # https://github.com/alvarobartt/investpy/issues/467

        self.stock = Security(self.stock_data['isin'])
        sleep(5)
        self.fund = Security(self.fund_data['isin'])
        sleep(5)
        self.currency_cross = Security(self.currency_cross_data['name'])
        sleep(5)

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

class TestMethod_get_security_price(unittest.TestCase):
    def setUp(self):
        self.from_date = datetime.date(year=2022, month=1, day=1)
        self.to_date = datetime.date(year=2022, month=1, day=9)

        self.msg_price = '{security}s stock price don\'t match at date {date}'

        # Time delay to avoid error code 429 
        # by breaching query limit of investing.com and being blacklisted for 24h
        # https://github.com/alvarobartt/investpy/issues/467

        self.securities = []
        self.securities.append(Security('SE0012673267'))    
        sleep(5)
        self.securities.append(Security('SE0012193019'))
        sleep(5)
        self.securities.append(Security('USD/SEK'))
        sleep(5)

        self.stock_with_from_date = Security('SE0012673267', datetime.date(year=2021, month=12, day=30))
        sleep(5)

        self.random_security_prices = {
            'Evolution Gaming': {
                datetime.date(year=2018, month=6,  day=8):  113.0,
                datetime.date(year=2020, month=2,  day=24): 407.0,
                datetime.date(year=2020, month=10, day=27): 690.0,
                datetime.date(year=2021, month=4,  day=29): 1666.2,
                datetime.date(year=2021, month=12,  day=3): 935.0
            },
            'Core Ny Teknik A': {
                datetime.date(year=2020, month=2,  day=24): 140.930,
                datetime.date(year=2020, month=10, day=27): 187.614,
                datetime.date(year=2021, month=4,  day=29): 236.883,
                datetime.date(year=2021, month=12,  day=3): 219.191
            },
            'USD/SEK': {
                datetime.date(year=2018, month=6,  day=8):  8.7081,
                datetime.date(year=2020, month=2,  day=24): 9.7319,
                datetime.date(year=2020, month=10, day=27): 8.7226,
                datetime.date(year=2021, month=4,  day=29): 8.3705,
                datetime.date(year=2021, month=12,  day=3): 9.1364
            }
            
        }
        self.security_price_range_short = {
            'Evolution Gaming': {
                datetime.date(year=2022, month=1, day=3): 1282.8,
                datetime.date(year=2022, month=1, day=4): 1282.0,
                datetime.date(year=2022, month=1, day=5): 1284.8,
                datetime.date(year=2022, month=1, day=7): 1184.8
            },
            'Core Ny Teknik A': {
                datetime.date(year=2022, month=1, day=3): 233.817,
                datetime.date(year=2022, month=1, day=4): 231.458,
                datetime.date(year=2022, month=1, day=5): 229.064,
                datetime.date(year=2022, month=1, day=7): 219.088
            },
            'USD/SEK': {
                datetime.date(year=2022, month=1, day=3): 9.1033,
                datetime.date(year=2022, month=1, day=4): 9.0871,
                datetime.date(year=2022, month=1, day=5): 9.1041,
                datetime.date(year=2022, month=1, day=6): 9.139,
                datetime.date(year=2022, month=1, day=7): 9.0428
            }
        }
        self.security_price_range_long = {
            'Evolution Gaming': {
                datetime.date(year=2022, month=1, day=1): 1286.2,
                datetime.date(year=2022, month=1, day=2): 1286.2,
                datetime.date(year=2022, month=1, day=3): 1282.8,
                datetime.date(year=2022, month=1, day=4): 1282.0,
                datetime.date(year=2022, month=1, day=5): 1284.8,
                datetime.date(year=2022, month=1, day=6): 1284.8,
                datetime.date(year=2022, month=1, day=7): 1184.8,
                datetime.date(year=2022, month=1, day=8): 1184.8,
                datetime.date(year=2022, month=1, day=9): 1184.8
            },
            'Core Ny Teknik A': {
                datetime.date(year=2022, month=1, day=1): 232.747,
                datetime.date(year=2022, month=1, day=2): 232.747,
                datetime.date(year=2022, month=1, day=3): 233.817,
                datetime.date(year=2022, month=1, day=4): 231.458,
                datetime.date(year=2022, month=1, day=5): 229.064,
                datetime.date(year=2022, month=1, day=6): 229.064,
                datetime.date(year=2022, month=1, day=7): 219.088,
                datetime.date(year=2022, month=1, day=8): 219.088,
                datetime.date(year=2022, month=1, day=9): 219.088
            },
            'USD/SEK': {
                datetime.date(year=2022, month=1, day=1): 9.0392,
                datetime.date(year=2022, month=1, day=2): 9.0392,
                datetime.date(year=2022, month=1, day=3): 9.1033,
                datetime.date(year=2022, month=1, day=4): 9.0871,
                datetime.date(year=2022, month=1, day=5): 9.1041,
                datetime.date(year=2022, month=1, day=6): 9.139,
                datetime.date(year=2022, month=1, day=7): 9.0428,
                datetime.date(year=2022, month=1, day=8): 9.0428,
                datetime.date(year=2022, month=1, day=9): 9.0578
            }   
        }

    def test_type(self):
        self.assertRaises(TypeError, self.securities[0].get_security_price(), None,      datetime.date(year=2021, month=5, day=5))
        self.assertRaises(TypeError, self.securities[0].get_security_price(), 'abc',     datetime.date(year=2021, month=5, day=5))
        self.assertRaises(TypeError, self.securities[0].get_security_price(), 1,         datetime.date(year=2021, month=5, day=5))
        self.assertRaises(TypeError, self.securities[0].get_security_price(), list(),    datetime.date(year=2021, month=5, day=5))

        self.assertRaises(TypeError, self.securities[0].get_security_price(), datetime.date(year=2021, month=5, day=5), None)
        self.assertRaises(TypeError, self.securities[0].get_security_price(), datetime.date(year=2021, month=5, day=5), 'abc')
        self.assertRaises(TypeError, self.securities[0].get_security_price(), datetime.date(year=2021, month=5, day=5), 1)
        self.assertRaises(TypeError, self.securities[0].get_security_price(), datetime.date(year=2021, month=5, day=5), list())

    def test_get_latest_security_price(self):
        results = self.securities[0].get_security_price()
        self.assertNotEqual(results, {})

    def test_get_security_price_output(self):
        for security in self.securities:
            for date in list(self.random_security_prices[security.get_basic_info()['name']].keys()):
                results = security.get_security_price(date)
                # test whether output is of length 1, i.e. stock price for a given day
                self.assertEqual(len(list(results.keys())), 1, msg='output is not for single day')

                # test whether stock price matches raw data
                self.assertEqual(
                    results[date], 
                    self.random_security_prices[security.get_basic_info()['name']][date], 
                    msg=self.msg_price.format(security= security.get_basic_info()['name'], date= date)
                )

    def test_get_security_historical_price_output(self):
        for security in self.securities:
            results = security.get_security_price(self.from_date, self.to_date)
            for date in list(self.security_price_range_short[security.get_basic_info()['name']].keys()):

                # test whether stock price matches raw data
                self.assertEqual(
                    results[date], 
                    self.security_price_range_short[security.get_basic_info()['name']][date], 
                    msg=self.msg_price.format(security= security.get_basic_info()['name'], date= date)
                )

    def test_get_security_historical_price_with_auto_fill_output(self):
        for security in self.securities:
            results = security.get_security_price(self.from_date, self.to_date, auto_fill= True)
            for date in list(self.security_price_range_long[security.get_basic_info()['name']].keys()):

                # test whether stock price matches raw data
                self.assertEqual(
                    results[date], 
                    self.security_price_range_long[security.get_basic_info()['name']][date], 
                    msg=self.msg_price.format(security= security.get_basic_info()['name'], date= date)
                )

    def test_get_security_historical_price_with_get_all_output(self):
        results = self.stock_with_from_date.get_security_price(get_all=True, auto_fill= False)
        for date in list(self.security_price_range_short[self.stock_with_from_date.get_basic_info()['name']].keys()):

            # test whether stock price matches raw data
            self.assertEqual(
                results[date], 
                self.security_price_range_short[self.stock_with_from_date.get_basic_info()['name']][date], 
                msg=self.msg_price.format(security= self.stock_with_from_date.get_basic_info()['name'], date= date)
            )

    def test_get_security_historical_price_with_get_all_and_auto_fill_output(self):
        self.security_price_range_long = {
            'Evolution Gaming': {
                datetime.date(year=2021, month=12, day=30): 1286.2,
                datetime.date(year=2021, month=12, day=31): 1286.2,
                datetime.date(year=2022, month=1, day=1): 1286.2,
                datetime.date(year=2022, month=1, day=2): 1286.2,
                datetime.date(year=2022, month=1, day=3): 1282.8,
                datetime.date(year=2022, month=1, day=4): 1282.0,
                datetime.date(year=2022, month=1, day=5): 1284.8,
                datetime.date(year=2022, month=1, day=6): 1284.8,
                datetime.date(year=2022, month=1, day=7): 1184.8,
                datetime.date(year=2022, month=1, day=8): 1184.8,
                datetime.date(year=2022, month=1, day=9): 1184.8
            }
        }
        results = self.stock_with_from_date.get_security_price(get_all=True, auto_fill= True)
        for date in list(self.security_price_range_long[self.stock_with_from_date.get_basic_info()['name']].keys()):

            # test whether stock price matches raw data
            self.assertEqual(
                results[date], 
                self.security_price_range_long[self.stock_with_from_date.get_basic_info()['name']][date], 
                msg=self.msg_price.format(security= self.stock_with_from_date.get_basic_info()['name'], date= date)
            )

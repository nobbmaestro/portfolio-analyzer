import unittest
import datetime

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




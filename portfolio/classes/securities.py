import investpy
import datetime
import json

class Security(object):
    def __init__(self, security):
        # Settings
        self.SUPPORTED_SECURITY_TYPES = (
            'stock',
            'fund', 
            'currency_cross'
        #    'index',
        #    'crypto', 
        #    'etf', 
        #    'bond', 
        #    'commodity', 
        #    'certificate',   
        )
        self.SECURITY_IDENTIFIED = False

        # Begin init
        if type(security) is not str:
            raise TypeError('arg not of type str')

        elif security == '':
            raise ValueError('arg cannot be empty')

        else:
            self.security = security
            try:
                self.name, self.full_name, self.security_type, self.isin, self.symbol, self.country, self.currency  = self.get_basic_info()
                self.latest_price = self.get_security_price()
                
            except RuntimeError as e:
                raise(RuntimeError(e))

    def __repr__(self):
        pass

    def get_security_price(self):
        pass


    def get_basic_info(self):
        def format_basic_info(security_type, basic_info):
            try:
                name = basic_info.to_dict()['name'][0]
            except KeyError:
                name = None

            try:
                full_name = basic_info.to_dict()['full_name'][0]
            except KeyError:
                full_name = None

            try:
                isin = basic_info.to_dict()['isin'][0]
            except KeyError:
                isin = None

            try:
                symbol = basic_info.to_dict()['symbol'][0]
            except KeyError:
                symbol = None

            try:
                country = basic_info.to_dict()['country'][0]
            except KeyError:
                country = None

            try:
                currency = basic_info.to_dict()['currency'][0]
            except KeyError:
                if security_type == 'currency_cross':
                    currency = name[4:]

                else:
                    currency = None

            return name, full_name, security_type, isin, symbol, country, currency
            
        
        if self.SECURITY_IDENTIFIED:
            return {
                'name'          : self.name,
                'full_name'     : self.full_name,
                'security_type' : self.security_type,
                'isin'          : self.isin,
                'symbol'        : self.symbol,
                'country'       : self.country,
                'currency'      : self.currency
                }

        else:
            for security_type in self.SUPPORTED_SECURITY_TYPES:
                try:
                    basic_info = eval(self.get_search_security_query_investpy(security_type, self.security))
                    if len(basic_info.index) == 1:
                        self.SECURITY_IDENTIFIED = True
                        return format_basic_info(security_type, basic_info)
                    else:
                        raise RuntimeError('several matched found')

                except RuntimeError as e:
                    if 'ERR#0043' in str(e):
                        pass
                    else:
                        raise RuntimeError(e)
            
            raise RuntimeError('no results were found for the introduced security')

        



    def get_search_security_query_investpy(self, security_type, security):
        """Prepares the investpy query, output ready to be used with eval().

        Args:
            security_type (str): Type for security. 
                Available types: 'stock', 'fund' or 'currency_cross'.
                Defaults to None.

            security (str): 
                If 'stock' or 'fund': ISIN of the security . 
                Defaults to None.

        Raises:
            ValueError: security type not supported.

        Returns:
            str: prepared query for investpy
        """
        q_search_security = {
                'stock'         : 'investpy.search_stocks(by= "isin", value= \"{security}\")',
                'fund'          : 'investpy.search_funds(by= "isin", value= \"{security}\")',
                'currency_cross': 'investpy.search_currency_crosses(by= "name", value= \"{security}\")'
            }
        if type(security_type) is not str or type(security) is not str:
            raise TypeError('arg not of type str.')

        elif security_type.lower() not in q_search_security.keys():
            raise ValueError('security type not supported.')

        else:
            return q_search_security[security_type.lower()].format(security= security.upper())

   
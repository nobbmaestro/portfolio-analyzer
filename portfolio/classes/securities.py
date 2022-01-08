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

            except RuntimeError as e:
                raise(RuntimeError(e))

    def __repr__(self):
        return self.name


    def get_security_price(self, from_date = datetime.date.today(), to_date = None):
        """Return a dictionary of the historical price for the given security. If no args given, return latest close price.

        Args:
            from_date (datetime.date, optional): user defined from date. Defaults to datetime.date.today().
            to_date (datetime.date, optional): user defined to date. Defaults to None.

        Raises:
            RuntimeError: security type not supported

        Returns:
            dict: with key datetime.date and value of the price as int
        """
        def format_security_price(price_data, only_last_row, auto_fill = False):
            price_data = price_data.Close.to_dict()
            formated_price_data = {}

            if only_last_row:
                last_row_index = list(price_data.keys())[-1]
                formated_price_data[datetime.date(year=last_row_index.year, month=last_row_index.month, day=last_row_index.day)] = price_data[last_row_index]

            else:
                for row_index in price_data.keys():
                    formated_price_data[datetime.date(year=row_index.year, month=row_index.month, day=row_index.day)] = price_data[row_index]
                    if auto_fill and (to_date - from_date + datetime.timedelta(days=1)) != datetime.timedelta(days=len(list(price_data.keys()))):
                        pass

            return formated_price_data
            
        if to_date == None:
            to_date = from_date
            from_date = from_date - datetime.timedelta(days=1)
    
        if self.security_type == 'stock':
            price_data = (
                eval(self.get_historical_data_query_investpy(
                    security_type= self.security_type, 
                    security=self.symbol, 
                    country=self.country,
                    from_date=from_date, 
                    to_date=to_date
                    )
                )
            )
        elif self.security_type == 'fund':
            price_data = (
                eval(self.get_historical_data_query_investpy(
                    security_type= self.security_type, 
                    security=self.name, 
                    country=self.country,
                    from_date=from_date, 
                    to_date=to_date
                    )
                )
            )
        elif self.security_type == 'currency_cross':
            price_data = (
                eval(self.get_historical_data_query_investpy(
                    security_type= self.security_type, 
                    security=self.name, 
                    country= None,
                    from_date=from_date, 
                    to_date=to_date, 
                    )
                )
            )
        else:
            raise RuntimeError('security type not supported')

        if (to_date - from_date) ==  datetime.timedelta(days=1) and len(price_data.index) > 1:
            return format_security_price(price_data, True)
                
        else:
            return format_security_price(price_data, False)

    def get_basic_info(self):
        """Returns basic information about the security

            Raises:
                RuntimeError: several matched found
                RuntimeError: no results were found for the given security'

            Returns:
                dict: containing name, full name, security type, isin, symbol, country and currency of the given security
        """
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
            
            raise RuntimeError('no results were found for the given security')

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

    def get_historical_data_query_investpy(self, security_type, security, country, from_date = datetime.date.today() - datetime.timedelta(days=1), to_date = datetime.date.today()):
        """Prepares the investpy query, output ready to be used with eval().

        Args:
            security_type (str): Type for security. 
                Available types: 'stock', 'fund' or 'currency_cross'.
                Defaults to None.

            security (str): 
                If 'stock' or 'fund': ISIN of the security . 
                Defaults to None.

            from_date (datetime.date, optional): 
                From date of the historical data. 
                Defaults to datetime.date.today() - datetime.timedelta.day(1).

            to_date (datetime.date, optional): 
                To date of the historical data. 
                Defaults to datetime.date.today().

            country ([str, optional): 
                Coubtry of the issued security. 
                Mandatory only for 'stock' and 'fund'. 
                Defaults to None.

        Raises:
            ValueError: [description]

        Returns:
            str: prepared query for investpy
        """
        q_historical_data = {
                'stock'         : "investpy.get_stock_historical_data(\"{security}\", country= \"{country}\", from_date= \"{from_date}\", to_date= \"{to_date}\")",
                'fund'          : 'investpy.get_fund_historical_data(\"{security}\", country= \"{country}\", from_date= \"{from_date}\", to_date= \"{to_date}\")',
                'currency_cross': 'investpy.get_currency_cross_historical_data(\"{security}\", from_date= \"{from_date}\", to_date= \"{to_date}\")',
            }
        if type(security_type) is not str or type(security) is not str:
            raise TypeError('arg not of type str.')

        elif country != None and type(country) is not str:
            raise TypeError('arg not of type str.')

        elif type(from_date) is not datetime.date:
            raise TypeError('dates not of type datetime.time')

        elif security_type not in q_historical_data.keys():
            raise ValueError('security type not supported.')

        else:
            if security_type in ['stock', 'fund']:
                return q_historical_data[security_type.lower()].format(security=security.upper(), country=country, from_date=self.__datetime_to_string(from_date), to_date=self.__datetime_to_string(to_date))
            else:
                return q_historical_data[security_type.lower()].format(security=security.upper(), from_date=self.__datetime_to_string(from_date), to_date=self.__datetime_to_string(to_date))


        
    def __datetime_to_string(self, date_value):
        """Converts datetime.date to str of format DD/MM/YYYY.

        Args:
            date_value (datetime.date): date

        Returns:
            str: converted date
        """
        if type(date_value) not in [datetime.date, datetime.datetime]:
            raise TypeError('Not a datetime')
        else:
            date_format = "{day}/{month}/{year}"
            return date_format.format(day=date_value.day, month=date_value.month, year=date_value.year)
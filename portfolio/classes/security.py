import investpy
import datetime
from dateutil.relativedelta import relativedelta
from portfolio.functions.find import find

class Security(object):
    def __init__(self, security, from_date= datetime.date(year=2015, month=1, day=1)):
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
        self.SECURITY_PRICE_OBTAINED = False

        if type(from_date) is not datetime.date:
            raise TypeError('from_date is not of type datetime.date')
        elif from_date > datetime.date.today():
            raise ValueError('from_date cannot exceed todays date')
        self.from_date = from_date

        # Begin init
        if type(security) is not str:
            raise TypeError('arg not of type str')

        elif security == '':
            raise ValueError('arg cannot be empty')

        else:
            self.security = security
            try:
                self.name, self.full_name, self.security_type, self.isin, self.symbol, self.country, self.currency  = self.get_security_info()
                self.historical_price = self.get_security_price()
 
            except RuntimeError as e:
                raise(RuntimeError(e))

    def __repr__(self):
        return self.name

    def get_security_info(self):
        """Returns basic information about the security

            Raises:
                RuntimeError: several matched found
                RuntimeError: no results were found for the given security'

            Returns:
                dict: containing name, full name, security type, isin, symbol, country and currency of the given security
        """
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
                    basic_info = eval(self.__get_search_security_query_investpy(security_type, self.security))
                    if len(basic_info.index) == 1:
                        self.SECURITY_IDENTIFIED = True
                        return self.__format_security_info(security_type, basic_info)
                    else:
                        raise RuntimeError('several matched found')

                except RuntimeError as e:
                    if 'ERR#0043' in str(e):
                        pass
                    else:
                        raise RuntimeError(e)
            
            raise RuntimeError('no results were found for the given security')


    def get_security_price(self, from_date = None, to_date = None, get_all = False, auto_fill = False):
        """Return a dictionary of the historical price of the security. If no args given, return latest close price.

        Usage:
            from_date = None, to_date = None, get_all = False: returns lasest close price
            from_date = None, to_date = None, get_all = True: return all available historical prices
            from_date != None, to_date = None: returns close price at given date
            from_date != None, to_date != None: returns close price between given dates

        Args:
            from_date (datetime.date, optional): user defined from date.
            to_date (datetime.date, optional): user defined to date.
            get_all (boolean, optional): If 'True', return all available historical prices. Defualts to 'False'.
            auto_fill (boolean, optional): If 'False', ignore holidays and non-trading days. Else if holiday or non-trading day, assigns price from latest trading day. Defaults to False.

        Raises:
            RuntimeError: security type not supported

        Returns:
            dict: 
                key (datetime.date): date index
                value (int): price at date index
        """
        if self.SECURITY_PRICE_OBTAINED:
            if from_date == None and to_date == None and get_all == False:
                return self.__format_security_price_by_date(datetime.date.today())

            if from_date == None and to_date == None and get_all == True:
                if auto_fill:
                    from_date = list(self.historical_price.keys())[0]
                    to_date = datetime.date.today()
                    return self.__format_security_price_by_date(from_date, to_date, auto_fill=True)
                else:
                    return self.historical_price

            elif from_date != None and to_date == None:
                return (self.__format_security_price_by_date(from_date, auto_fill=False))

            elif from_date != None and to_date != None:
                return self.__format_security_price_by_date(from_date, to_date, auto_fill)

        else:
            to_date   = datetime.date.today() 
            price_data = (eval(self.__get_historical_data_query_investpy(from_date=self.from_date, to_date=to_date)))                

            self.SECURITY_PRICE_OBTAINED = True
            return self.__format_security_price(price_data)

    def get_security_return(self, time_frame = 'YTD'):
        """Returns the return of the security for the given timeframe

        Supported timeframes:
            YTD: Return from Year-to-Date,
            1D: Return last trading day,
            1W: Return last week,
            1M: Return last month,
            3M: Return last three months,
            6M: Return last six months,
            1Y: Return last year,
            3Y: Return last three years,
            MAX: Return since initial public offering (IPO)
            CAGR: Compound Annual Growth Rate 
            datetime.date: Return from given date
            
        Args:
            time_frame (str, optional): [description]. Defaults to 'YTD'.

        Raises:
            ValueError: [description]

        Returns:
            str: return as percentage from given timeframe
        """
        if type(time_frame) not in [str, datetime.date]:
            raise TypeError('arg must be of type str or datetime.date') 

        elif type(time_frame) is str:
            time_frame = time_frame.upper()

        try:
            if time_frame == '1D':
                date = datetime.date.today() - datetime.timedelta(days=1)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date)
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == 'YTD':
                date = datetime.date(year=datetime.date.today().year, month=1, day=1)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date)
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == '1W':
                date = datetime.date.today() - datetime.timedelta(weeks=1)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == '1M':
                date = datetime.date.today() - relativedelta(months=+1)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == '3M':
                date = datetime.date.today() - relativedelta(months=+3)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == '6M':
                date = datetime.date.today() - relativedelta(months=+6)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == '1Y':
                date = datetime.date.today() - relativedelta(years=+1)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == '3Y':
                date = datetime.date.today() - relativedelta(years=+3)
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(date) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1) 

            elif time_frame == 'MAX':
                data = self.get_security_price(get_all=True) 
                ending_value = data[list(data.keys())[-1]]
                beginning_value = data[list(data.keys())[0]]
                return "{:.2%}".format(ending_value/beginning_value - 1)

            elif time_frame == 'CAGR':
                # Formula: CAGR = (EV/BV)^(1/n) - 1, where n is the number of years
                ending_value = self.get_security_price()
                ending_date = list(ending_value.keys())[0]

                beginning_value = self.get_security_price(get_all=True) 
                beginning_date = list(beginning_value.keys())[0]
                n = (ending_date - beginning_date).days / 365

                return "{:.2%}".format((ending_value[ending_date]/beginning_value[beginning_date]) ** (1/n) - 1)

            elif type(time_frame) == datetime.date:
                ending_value = self.get_security_price()
                beginning_value = self.get_security_price(time_frame) 
                return "{:.2%}".format(ending_value[list(ending_value.keys())[0]] / beginning_value[list(beginning_value.keys())[0]] - 1)

            else:
                raise ValueError('Incorrect function')
        
        except ValueError as e:
            # If time_frame exceeds availble price data, target out-of-bounds error will be raised. 
            # Then return None
            if str(e) == "target out-of-bounds":
                return None

            else:
                raise RuntimeError

    def __format_security_info(self, security_type, basic_info):
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

    def __format_security_price(self, price_data):
        """Converts price data from pandas.DataFrame to dict

        Args:
            price_data (pandas.DataFrame): price data

        Returns:
            dict: 
                key (datetime.date): date index
                value (int): price at date index
        """
        price_data = price_data.Close.to_dict()
        formated_price_data = {}

        for row_index in price_data.keys():
            formated_price_data[datetime.date(year=row_index.year, month=row_index.month, day=row_index.day)] = price_data[row_index]

        return formated_price_data

    def __format_security_price_by_date(self, from_date, to_date= None, auto_fill= False):
        """Returns formated security prices between given dates.

        Usage:
            from_date != None, to_date = None: returns latest close price
            from_date != None, to_date != None, auto_fill = False: returns close price between given dates
            from_date != None, to_date != None, auto_fill = False: returns close price between given dates with ignored non-trading days
            
        Args:
            from_date ([type]): user defined from date.
            to_date ([type], optional): user defined to date. Defaults to None.
            auto_fill (bool, optional): If 'False', ignore holidays and non-trading days. Else if holiday or non-trading day, assigns price from latest trading day. Defaults to False.

        Raises:
            ValueError: arg cannot exceed exceed todays date

        Returns:
            dict: 
                key (datetime.date): date index
                value (int): price at date index
        """
        formated_price_data = {}
        list_of_dates = list(self.historical_price.keys())
        
        # if auto_fill requested, get the last trading day prior to from_date
        # else, get first trading day after from_date
        if auto_fill == False and to_date == None or auto_fill:
            from_index = find(data= list_of_dates, target= from_date, low= 0, high= len(list_of_dates) - 1, force=False)
        else:
            from_index = find(data= list_of_dates, target= from_date, low= 0, high= len(list_of_dates) - 1, force=False) + 1
        
        # if to_date is given, get the last trading day prior to to_date
        # else, to_date shall be set to from_date and return security price on from_date
        if to_date != None:
            if to_date <= datetime.date.today():
                to_index = find(data= list_of_dates, target= to_date, low= 0, high= len(list_of_dates) - 1, force=False)
            else:
                raise ValueError('arg cannot exceed exceed todays date')
        else:
            to_index = from_index

        for i in range(from_index, to_index + 1):
            # print(list_of_dates[i])
            if auto_fill == False:
                formated_price_data[list_of_dates[i]] = self.historical_price[list_of_dates[i]]

            else:
                # i + 1 may cause IndexError, pass if IndexError is raised
                try:
                    # if date at index i is not the next week day at index i+1
                    if list_of_dates[i] + datetime.timedelta(days=1) != list_of_dates[i + 1]:

                        # insert j number of days between date at index i and i+1 with price at index i
                        for j in range((list_of_dates[i+1] - list_of_dates[i]).days):
                            filler_day = list_of_dates[i] + datetime.timedelta(days=j)
                            if filler_day >= from_date and filler_day <= to_date:
                                formated_price_data[filler_day] = self.historical_price[list_of_dates[i]]
                                # print('\t', filler_day)

                    else:
                        formated_price_data[list_of_dates[i]] = self.historical_price[list_of_dates[i]]

                except IndexError:
                    # if to_date is highier than last date of list_of_dates, 
                    # then fill insert last trading day close price until to_date
                    if i == to_index:
                        for k in range((to_date - list_of_dates[i]).days + 1):
                            filler_day = list_of_dates[i] + datetime.timedelta(days=k)
                            formated_price_data[filler_day] = self.historical_price[list_of_dates[i]]
                            # print('\t', filler_day)

        return formated_price_data
  
    def __get_search_security_query_investpy(self, security_type, security):
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

    def __get_historical_data_query_investpy(self, from_date, to_date):
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
        if type(self.security_type) is not str or type(self.security) is not str:
            raise TypeError('arg not of type str.')

        elif self.country != None and type(self.country) is not str:
            raise TypeError('arg not of type str.')

        elif type(from_date) is not datetime.date:
            raise TypeError('dates not of type datetime.time')

        elif self.security_type not in q_historical_data.keys():
            raise ValueError('security type not supported.')

        else:
            if self.security_type == 'stock':
                return q_historical_data[self.security_type.lower()].format(security=self.symbol, country=self.country, from_date=self.__datetime_to_string(from_date), to_date=self.__datetime_to_string(to_date))
            elif self.security_type == 'fund':
                return q_historical_data[self.security_type.lower()].format(security=self.name, country=self.country, from_date=self.__datetime_to_string(from_date), to_date=self.__datetime_to_string(to_date))
            else:
                return q_historical_data[self.security_type.lower()].format(security=self.security, from_date=self.__datetime_to_string(from_date), to_date=self.__datetime_to_string(to_date))

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
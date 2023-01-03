import pandas as pd
import datetime as dt
import os

class db:
    def __init__(self):
        self.transactions = db.values_init('transactions')
        self.cc = pd.read_csv(r'db\country_codes.csv', index_col=0)
        self.customers = db.values_init('customers')
        self.prod_info = pd.read_csv(r'db\prod_cat_info.csv')

    @staticmethod
    def values_init(x):

        def convert_dates(y):
            try:
                return dt.datetime.strptime(y, '%d-%m-%Y')
            except:
                return dt.datetime.strptime(y, '%d/%m/%Y')

        def convert_day(y):

            return dt.datetime.weekday(y)

        values = pd.DataFrame()
        if x == 'transactions':
            src = r'db\transactions'
            for filename in os.listdir(src):
                values = values.append(pd.read_csv(os.path.join(src, filename), index_col=0))

            values['tran_date'] = values['tran_date'].apply(lambda y: convert_dates(y))
            values['day'] = values['tran_date'].apply(lambda y: convert_day(y))

        elif x == 'customers':
            customers = pd.read_csv(r'db\customers.csv', index_col=0)
            values = pd.DataFrame(customers)

            values['DOB'] = values['DOB'].apply(lambda y: convert_dates(y))

        return values

    def merge(self):
        df = self.transactions.join(
            self.prod_info.drop_duplicates(subset=['prod_cat_code']).set_index('prod_cat_code')['prod_cat'],
            on='prod_cat_code', how='left')

        df = df.join(
            self.prod_info.drop_duplicates(subset=['prod_sub_cat_code']).set_index('prod_sub_cat_code')['prod_subcat'],
            on='prod_subcat_code', how='left')

        df = df.join(self.customers.join(self.cc, on='country_code').set_index('customer_Id'), on='cust_id')

        self.merged = df


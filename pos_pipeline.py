import pandas as pd
import glob
import os

# assuming that a weekly data folder containing 3 csv files (one for each days for 3 days) is provided
days = ['10012019', '10022019', '10032019'] 
sales = ['Sales_locationid_'+ i + '.csv' for i in days]
sales_payments = ['SalesPayment_locationid_'+ i + '.csv' for i in days]
sales_details = ['SalesDetails_locationid_'+ i + '.csv' for i in days]

# using glob instead
sales_dir = '~/POS/Sales'
sales_pmt_dir = '~/POS/SalesPayments'
sales_details_dir = '~/POS/SalesDetails'

sales_csv = sorted(glob.glob(os.path.join(sales_dir, '*.csv')))
sales_pmt_csv = sorted(glob.glob(os.path.join(sales_pmt_dir, '*.csv')))
sales_details_csv = sorted(glob.glob(os.path.join(sales_details_dir, '*.csv')))

# function to read files iteratively
def read_csv(file):
    df = []
    for f in file:
        df.append(pd.read_csv(f))
    return(df)

# read in Sales file 
sales_df = read_csv(sales_csv)

# read in Sales Payments file
sales_pmt_df = read_csv(sales_pmt_csv)

# read in Sales Details file
sales_details_df = read_csv(sales_details_csv)

# read in Employee file
employees = pd.read_csv('~/POS/Employees.csv', usecols = ['First Name', 'POSID'])

# combine csv files
df_comb = []
for i in range(len(sales_df)):
    df_comb.append(sales_df[i].merge(sales_pmt_df[i], how = 'inner', on = 'Receipt Number').merge(sales_details_df[i], how = 'right', on = 'Receipt Number'))
    # parse date data
    df_comb[i]['Date_x'] = pd.to_datetime(df_comb[i]['Date_x'])
    # clean up
    df_comb[i].rename(columns = {'Amount_x': 'Receipt Total', 'Amount_y': 'Item Price', 'Date_x': 'Date'}, inplace = True)
    df_comb[i].drop(columns = ['Date_y'], inplace = True)
    df_comb[i]['Day of Week'] = df_comb[i]['Date'].dt.weekday_name
    df_comb[i]['Time of Day'] = df_comb[i]['Date'].dt.hour
    
# concatenate dataframes
data_comb = pd.concat(df_comb)



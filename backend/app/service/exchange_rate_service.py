from datetime import datetime
from app.constant import EXCHANGE_RATE_COLLECTION_NAME, STOCK_FILE_PATH, OUTPUT_STOCK_FILE_PATH
import pandas as pd
import pytz  # For handling timezone-aware datetimes

class ExchangeRateService:
    def __init__(self, mongo_client, file_path):
        self.mongo_client = mongo_client
        self.collection = self.mongo_client.get_collection(EXCHANGE_RATE_COLLECTION_NAME)
        self.file_path = file_path

    
    def read_exchange_rates_from_csv(self) -> pd.DataFrame:
        """
        Reads a CSV file containing date and exchange rate columns and returns a DataFrame.
        
        :param file_path: Path to the CSV file
        :return: A pandas DataFrame with columns 'date' and 'rate'
        """
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(self.file_path)
            # Check if the required columns are present
            if 'date' not in df.columns or 'rate' not in df.columns:
                raise ValueError("CSV file must contain 'date' and 'rate' columns.")
            
            # Convert 'date' column to datetime format
            df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y')

            df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
            
            df.dropna(inplace=True)

            return df
    
        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def insert_exchange_rate(self):
        try:
            # Read exchange rates from CSV
            df = self.read_exchange_rates_from_csv()
            
            if df.empty:
                print("No data to insert.")
                return

            # Get existing dates from MongoDB
            existing_dates = self.collection.distinct('date')
            existing_dates = set(pd.to_datetime(existing_dates))  # Convert to datetime objects for comparison

            # Filter out rows with existing dates
            df['date'] = pd.to_datetime(df['date'])  # Ensure date is in datetime format
            new_exchange_rate = df[~df['date'].isin(existing_dates)]
            
            if new_exchange_rate.empty:
                print("All dates are already in the database.")
                return
            
            # Prepare data for insertion
            records = new_exchange_rate.to_dict(orient='records')
            
            # Insert data into MongoDB
            self.collection.insert_many(records)
            
            print("New data inserted successfully.")
        
        except Exception as e:
            print(f"An error occurred while inserting data into MongoDB: {e}")

    ## find the date in the rate_dict, if the date is not available
    ## Use the nearest previous rate
    def get_rate(self, date, rate_dict, sorted_dates):
        if date in rate_dict:
            return rate_dict[date]

        date_obj = datetime.strptime(date, "%Y-%m-%d")
        # Find the closest previous date
        for d in reversed(sorted_dates):
            if d < date_obj:
                return rate_dict[d]
        
        # If no previous date is found
        return None
    
    def export_stock_value_based_on_exchange(self):
            ## initiate exchange rate and save to database
            self.insert_exchange_rate()

            # Fetch exchange rates from MongoDB
            rates = self.collection.find()
            rate_dict = {rate['date']: rate['rate'] for rate in rates}

            print(rate_dict)
            # Read Excel file
            stock_df = pd.read_csv(STOCK_FILE_PATH)

            # Ensure the columns are named 'date' and 'dollar'
            if 'Proceeds' not in stock_df.columns or 'Date/Time' not in stock_df.columns:
                raise ValueError("Excel file must contain 'date' and 'dollar' columns")

            stock_df = stock_df[~stock_df['Symbol'].str.startswith('Total', na=False)]

            # Convert the 'date' column to datetime format
            stock_df['Date/Time'] = pd.to_datetime(stock_df['Date/Time']).dt.strftime('%Y-%m-%d')

            sorted_dates = sorted(rate_dict.keys())
            # Perform the exchange rate calculation
            # stock_df['rate'] = stock_df['Date/Time'].map(rate_dict)
            stock_df['rate'] = stock_df['Date/Time'].apply(lambda x: self.get_rate(x, rate_dict, sorted_dates))


            
            # replaced "," and convert to numeric
            stock_df['Proceeds'] = pd.to_numeric(stock_df['Proceeds'].str.replace(',', ''), errors='coerce')
            stock_df['exchanged_dollar'] = stock_df['Proceeds'] / stock_df['rate']

            # Drop rows where rate is not available
            # stock_df = stock_df.dropna(subset=['rate'])
            
            stock_df = stock_df.sort_values(by=['Symbol', 'Date/Time'])
            # Save to CSV
            stock_df.to_csv(OUTPUT_STOCK_FILE_PATH, index=False)

            print(f"Exchange calculations saved to {OUTPUT_STOCK_FILE_PATH}")



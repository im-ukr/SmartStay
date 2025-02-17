# preprocess_clv_data.py
import os
import pandas as pd
from datetime import datetime

def process_clv_data():
    csv_folder = 'csv_files'

    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    current_time = datetime.now()

    file_name = 'csv_files/final-rectfied-clv-data.csv'
    df1 = pd.read_csv(file_name)

    df1['check_out_date'] = pd.to_datetime(df1['check_out_date'], errors='coerce')

    # Step 1
    df1['frequency_of_bookings'] = df1.groupby('guest_id')['guest_id'].transform('count')

    # Step 2
    df1['days_since_last_booking'] = df1.groupby('guest_id')['check_out_date'].transform(
        lambda x: (pd.to_datetime(current_time) - x.iloc[-1]).days if pd.notna(x.iloc[-1]) else None
    )
    # Step 3
    df1['total_revenue_generated'] = df1.groupby('guest_id')['grand_total_amount'].transform('sum')

    # Step 4
    df1['average_stay_duration'] = df1.groupby('guest_id')['duration_of_stay'].transform('mean')

    # Step 5
    df1['total_meal_charges'] = df1.groupby('guest_id')['meal_charges'].transform('sum')

    # Step 6
    df1['total_revenue_generated'] = df1['total_revenue_generated'].round(2)
    df1['average_stay_duration'] = df1['average_stay_duration'].round(2)
    df1['total_meal_charges'] = df1['total_meal_charges'].round(2)

    result_df = df1[['guest_id', 'guest_name', 'email_id', 'frequency_of_bookings', 
                     'days_since_last_booking', 
                     'average_stay_duration', 'total_meal_charges','total_revenue_generated']].drop_duplicates().reset_index(drop=True)

    result_df.to_csv(os.path.join(csv_folder, 'condensed-clv-data.csv'), index=False)
    df1.to_csv(os.path.join(csv_folder, 'final-clv-data.csv'), index=False)
import sqlite3
import csv
import os

DB_NAME = 'hotel_booking.db'
CSV_FILE = 'hotel_bookings.csv'

def load_data():
    if not os.path.exists(CSV_FILE):
        print(f"Error: '{CSV_FILE}' not found in the current folder.")
        print("   Please download hotel_bookings.csv from Kaggle and place it here.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"Found {CSV_FILE}. Loading data into database... (this may take 20-40 seconds)")

    # Create a simple flat table that matches the Kaggle dataset
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BOOKINGS (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel TEXT,
            is_canceled INTEGER,
            lead_time INTEGER,
            arrival_date_year INTEGER,
            arrival_date_month TEXT,
            arrival_date_week_number INTEGER,
            arrival_date_day_of_month INTEGER,
            stays_in_weekend_nights INTEGER,
            stays_in_week_nights INTEGER,
            adults INTEGER,
            children REAL,
            babies INTEGER,
            meal TEXT,
            country TEXT,
            market_segment TEXT,
            distribution_channel TEXT,
            is_repeated_guest INTEGER,
            previous_cancellations INTEGER,
            previous_bookings_not_canceled INTEGER,
            reserved_room_type TEXT,
            assigned_room_type TEXT,
            booking_changes INTEGER,
            deposit_type TEXT,
            agent TEXT,
            company TEXT,
            days_in_waiting_list INTEGER,
            customer_type TEXT,
            adr REAL,
            required_car_parking_spaces INTEGER,
            total_of_special_requests INTEGER,
            reservation_status TEXT,
            reservation_status_date TEXT
        )
    ''')

    # Read and insert the CSV data
    with open(CSV_FILE, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  

        placeholders = ','.join(['?'] * len(headers))
        insert_sql = f"INSERT INTO BOOKINGS VALUES (NULL, {placeholders})"

        row_count = 0
        for row in reader:
            # Convert empty strings to None (NULL in SQLite)
            cleaned_row = [None if val == '' else val for val in row]
            cursor.execute(insert_sql, cleaned_row)
            row_count += 1
            
            if row_count % 10000 == 0:
                print(f"   Loaded {row_count:,} bookings so far...")

    conn.commit()
    conn.close()

    print(f"\n Loaded {row_count:,} hotel bookings into the database.")

if __name__ == "__main__":
    load_data()
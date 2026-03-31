import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database"
)

cursor = conn.cursor()

def clean_dataframe(df):
    df = df.where(pd.notnull(df), None)
    return df

def load_table(csv_file, insert_query):
    df = pd.read_csv(csv_file)
    df = clean_dataframe(df)
    data = [tuple(row) for row in df.to_numpy()]
    cursor.executemany(insert_query, data)
    conn.commit()

load_table(
    "data/hotel.csv",
    "INSERT INTO HOTEL (hotel_id, hotel_name, hotel_type, address) VALUES (%s, %s, %s, %s)"
)

load_table(
    "data/guest.csv",
    "INSERT INTO GUEST (guest_id, first_name, last_name, email, country) VALUES (%s, %s, %s, %s, %s)"
)

load_table(
    "data/room.csv",
    "INSERT INTO ROOM (room_id, room_type, capacity, base_price) VALUES (%s, %s, %s, %s)"
)

booking_df = pd.read_csv("data/booking.csv")
booking_df = clean_dataframe(booking_df)

if 'arrival_date' in booking_df.columns:
    booking_df['arrival_date'] = pd.to_datetime(booking_df['arrival_date'], errors='coerce')
    booking_df['arrival_date'] = booking_df['arrival_date'].dt.strftime('%Y-%m-%d')

booking_data = [tuple(row) for row in booking_df.to_numpy()]

cursor.executemany(
    "INSERT INTO BOOKING (booking_id, hotel_id, guest_id, arrival_date, lead_time, is_canceled, adr) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    booking_data
)
conn.commit()

load_table(
    "data/booking_room.csv",
    "INSERT INTO BOOKING_ROOM (booking_id, room_id, price_at_booking, number_of_rooms) VALUES (%s, %s, %s, %s)"
)

load_table(
    "data/stay_detail.csv",
    "INSERT INTO STAY_DETAIL (booking_id, weekend_nights, week_nights) VALUES (%s, %s, %s)"
)

cursor.close()
conn.close()

print("Data successfully loaded into database.")

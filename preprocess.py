import pandas as pd
import numpy as np

df = pd.read_csv("hotel_bookings.csv")

# ---------------- HOTEL ----------------
hotel_df = df[['hotel']].drop_duplicates().reset_index(drop=True)
hotel_df['hotel_id'] = hotel_df.index + 1
hotel_df['hotel_name'] = hotel_df['hotel']
hotel_df['hotel_type'] = hotel_df['hotel']
hotel_df['address'] = None

hotel_df[['hotel_id','hotel_name','hotel_type','address']].to_csv("data/hotel.csv", index=False)

# ---------------- GUEST ----------------
guest_df = df[['country']].copy()
guest_df['guest_id'] = range(1, len(guest_df)+1)
guest_df['first_name'] = "Guest"
guest_df['last_name'] = guest_df['guest_id'].astype(str)
guest_df['email'] = None

guest_df[['guest_id','first_name','last_name','email','country']].to_csv("data/guest.csv", index=False)

# ---------------- ROOM ----------------
room_types = df[['reserved_room_type']].drop_duplicates().reset_index(drop=True)
room_types['room_id'] = room_types.index + 1
room_types['room_type'] = room_types['reserved_room_type']
room_types['capacity'] = np.random.randint(1, 5, size=len(room_types))
room_types['base_price'] = np.random.randint(50, 300, size=len(room_types))

room_types[['room_id','room_type','capacity','base_price']].to_csv("data/room.csv", index=False)

# ---------------- BOOKING ----------------
booking_df = df.copy()
booking_df['booking_id'] = range(1, len(df)+1)

# map hotel_id
booking_df = booking_df.merge(hotel_df[['hotel_id','hotel_name']],
                              left_on='hotel',
                              right_on='hotel_name',
                              how='left')

booking_df['arrival_date'] = pd.to_datetime(
    booking_df['arrival_date_year'].astype(str) + "-" +
    booking_df['arrival_date_month'] + "-" +
    booking_df['arrival_date_day_of_month'].astype(str),
    errors='coerce'
)

booking_df[['booking_id','hotel_id','guest_id','arrival_date',
            'lead_time','is_canceled','adr']].to_csv("data/booking.csv", index=False)

# ---------------- BOOKING_ROOM ----------------
booking_room_df = booking_df[['booking_id','reserved_room_type','adr']].copy()
booking_room_df = booking_room_df.merge(room_types[['room_id','room_type']],
                                        left_on='reserved_room_type',
                                        right_on='room_type')

booking_room_df['price_at_booking'] = booking_room_df['adr']
booking_room_df['number_of_rooms'] = 1

booking_room_df[['booking_id','room_id','price_at_booking','number_of_rooms']].to_csv("data/booking_room.csv", index=False)

# ---------------- STAY_DETAIL ----------------
stay_df = booking_df[['booking_id','stays_in_weekend_nights','stays_in_week_nights']]
stay_df.columns = ['booking_id','weekend_nights','week_nights']

stay_df.to_csv("data/stay_detail.csv", index=False)

import sqlite3
import os

DB_NAME = 'hotel_booking.db'

def connect_db():
    if not os.path.exists(DB_NAME):
        print(f"Database '{DB_NAME}' not found.")
        print("   Please run load_data.py first to create and populate the database.")
        exit(1)
    
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Easier rows, remember for later pls
    return conn

def main_menu():
    print("\n" + "="*60)
    print("   HOTEL BOOKING MANAGEMENT AND ANALYTICS SYSTEM")
    print("="*60)
    print("1. View All Bookings (with Hotel & Arrival Info)")
    print("2. Search Bookings by Arrival Year Range")
    print("3. View Room & Stay Details for a Specific Booking")
    print("4. Analyze Average ADR (Daily Rate) by Hotel")
    print("5. View Stay Summary for a Specific Booking")
    print("0. Exit")
    print("="*60)
    choice = input("Enter your choice (0-5): ").strip()
    return choice

def feature1(conn):
    """Feature 1: View All Bookings with Hotel Info"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT booking_id, 
               hotel,
               arrival_date_year || '-' || arrival_date_month || '-' || arrival_date_day_of_month AS arrival_date,
               is_canceled,
               lead_time,
               adr
        FROM BOOKINGS
        ORDER BY arrival_date_year DESC, arrival_date_month, arrival_date_day_of_month DESC
        LIMIT 30
    ''')
    rows = cursor.fetchall()
    
    print("\n=== ALL BOOKINGS (Most Recent 30) ===")
    print(f"{'ID':<6} {'Hotel':<15} {'Arrival Date':<15} {'Canceled':<8} {'Lead Time':<9} {'ADR':<8}")
    print("-" * 70)
    for row in rows:
        print(f"{row['booking_id']:<6} {row['hotel']:<15} {row['arrival_date']:<15} "
              f"{row['is_canceled']:<8} {row['lead_time']:<9} ${row['adr']:.2f}")

def feature2(conn):
    """Feature 2: Search Bookings by Arrival Year Range"""
    try:
        start_year = int(input("Enter start year (e.g. 2015): "))
        end_year = int(input("Enter end year (e.g. 2017): "))
    except ValueError:
        print("Not a valid year.")
        return
    
    cursor = conn.cursor()
    cursor.execute('''
        SELECT booking_id, 
               hotel,
               arrival_date_year || '-' || arrival_date_month || '-' || arrival_date_day_of_month AS arrival_date,
               is_canceled,
               lead_time,
               adr
        FROM BOOKINGS
        WHERE arrival_date_year BETWEEN ? AND ?
        ORDER BY arrival_date_year, arrival_date_month, arrival_date_day_of_month
        LIMIT 50
    ''', (start_year, end_year))
    rows = cursor.fetchall()
    
    print(f"\n=== BOOKINGS FROM {start_year} TO {end_year} ({len(rows)} shown) ===")
    print(f"{'ID':<6} {'Hotel':<15} {'Arrival Date':<15} {'Canceled':<8} {'Lead Time':<9} {'ADR':<8}")
    print("-" * 70)
    for row in rows:
        print(f"{row['booking_id']:<6} {row['hotel']:<15} {row['arrival_date']:<15} "
              f"{row['is_canceled']:<8} {row['lead_time']:<9} ${row['adr']:.2f}")

def feature3(conn):
    """Feature 3: View Room & Stay Details for a Booking"""
    booking_id = input("Enter Booking ID: ").strip()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT booking_id,
               hotel,
               reserved_room_type,
               assigned_room_type,
               stays_in_weekend_nights,
               stays_in_week_nights,
               adults,
               children,
               babies,
               adr
        FROM BOOKINGS
        WHERE booking_id = ?
    ''', (booking_id,))
    row = cursor.fetchone()
    
    if row:
        print(f"\n=== ROOM & STAY DETAILS FOR BOOKING {booking_id} ===")
        print(f"Hotel                  : {row['hotel']}")
        print(f"Reserved Room Type     : {row['reserved_room_type']}")
        print(f"Assigned Room Type     : {row['assigned_room_type']}")
        print(f"Weekend Nights         : {row['stays_in_weekend_nights']}")
        print(f"Week Nights            : {row['stays_in_week_nights']}")
        print(f"Total Nights           : {row['stays_in_weekend_nights'] + row['stays_in_week_nights']}")
        print(f"Adults / Children / Babies : {row['adults']} / {row['children']} / {row['babies']}")
        print(f"Average Daily Rate     : ${row['adr']:.2f}")
    else:
        print("Booking ID not found.")

def feature4(conn):
    """Feature 4: Analyze Average ADR by Hotel"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT hotel,
               ROUND(AVG(adr), 2) AS avg_adr,
               COUNT(*) AS total_bookings,
               ROUND(AVG(lead_time), 1) AS avg_lead_time
        FROM BOOKINGS
        GROUP BY hotel
        ORDER BY avg_adr DESC
    ''')
    rows = cursor.fetchall()
    
    print("\n=== AVERAGE ADR BY HOTEL ===")
    print(f"{'Hotel':<20} {'Avg ADR':<10} {'Bookings':<10} {'Avg Lead Time':<15}")
    print("-" * 60)
    for row in rows:
        print(f"{row['hotel']:<20} ${row['avg_adr']:<9} {row['total_bookings']:<10} {row['avg_lead_time']:<15} days")

def feature5(conn):
    """Feature 5: View Stay Summary for a Specific Booking"""
    booking_id = input("Enter Booking ID: ").strip()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT booking_id,
               hotel,
               stays_in_weekend_nights,
               stays_in_week_nights,
               (stays_in_weekend_nights + stays_in_week_nights) AS total_nights,
               customer_type,
               is_repeated_guest,
               total_of_special_requests
        FROM BOOKINGS
        WHERE booking_id = ?
    ''', (booking_id,))
    row = cursor.fetchone()
    
    if row:
        print(f"\n=== STAY SUMMARY FOR BOOKING {booking_id} ===")
        print(f"Hotel                     : {row['hotel']}")
        print(f"Weekend Nights            : {row['stays_in_weekend_nights']}")
        print(f"Week Nights               : {row['stays_in_week_nights']}")
        print(f"Total Nights              : {row['total_nights']}")
        print(f"Customer Type             : {row['customer_type']}")
        print(f"Repeated Guest            : {'Yes' if row['is_repeated_guest'] == 1 else 'No'}")
        print(f"Special Requests          : {row['total_of_special_requests']}")
    else:
        print("Booking ID not found.")

def main():
    print("Connecting to Hotel Booking Database...")
    conn = connect_db()
    print("Connected successfully.\n")
    
    while True:
        choice = main_menu()
        if choice == '1':
            feature1(conn)
        elif choice == '2':
            feature2(conn)
        elif choice == '3':
            feature3(conn)
        elif choice == '4':
            feature4(conn)
        elif choice == '5':
            feature5(conn)
        elif choice == '0':
            print("\nThank you for using the Hotel Booking System. Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number 0-5.")
        
        input("\nPress Enter to return to the main menu...")

    conn.close()

if __name__ == "__main__":
    main()
import sqlite3

def connect_db():
    return sqlite3.connect("hotel.db")

def feature1():
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT b.booking_id, g.first_name, g.last_name, h.hotel_name, b.arrival_date, b.is_canceled
    FROM BOOKING b
    JOIN GUEST g ON b.guest_id = g.guest_id
    JOIN HOTEL h ON b.hotel_id = h.hotel_id;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()


def feature2():
    start = input("Enter start date (YYYY-MM-DD): ")
    end = input("Enter end date (YYYY-MM-DD): ")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT booking_id, arrival_date, lead_time, adr
    FROM BOOKING
    WHERE arrival_date BETWEEN ? AND ?;
    """

    cursor.execute(query, (start, end))
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()


def feature3():
    booking_id = input("Enter booking ID: ")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT br.booking_id, r.room_type, br.number_of_rooms, br.price_at_booking
    FROM BOOKING_ROOM br
    JOIN ROOM r ON br.room_id = r.room_id
    WHERE br.booking_id = ?;
    """

    cursor.execute(query, (booking_id,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()


def feature4():
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT h.hotel_name, AVG(b.adr)
    FROM BOOKING b
    JOIN HOTEL h ON b.hotel_id = h.hotel_id
    GROUP BY h.hotel_name;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()


def feature5():
    booking_id = input("Enter booking ID: ")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT b.booking_id, sd.weekend_nights, sd.week_nights
    FROM STAY_DETAIL sd
    JOIN BOOKING b ON sd.booking_id = b.booking_id
    WHERE b.booking_id = ?;
    """

    cursor.execute(query, (booking_id,))
    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()


def menu():
    while True:
        print("\n--- HOTEL DATABASE MENU ---")
        print("1. View all bookings")
        print("2. Search bookings by date range")
        print("3. View rooms for a booking")
        print("4. Average ADR by hotel")
        print("5. View stay details")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            feature1()
        elif choice == "2":
            feature2()
        elif choice == "3":
            feature3()
        elif choice == "4":
            feature4()
        elif choice == "5":
            feature5()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

menu()

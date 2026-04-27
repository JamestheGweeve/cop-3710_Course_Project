DROP TABLE IF EXISTS STAY_DETAIL;
DROP TABLE IF EXISTS BOOKING_ROOM;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS ROOM;
DROP TABLE IF EXISTS GUEST;
DROP TABLE IF EXISTS HOTEL;

CREATE TABLE HOTEL (
    hotel_id INT PRIMARY KEY,
    hotel_name VARCHAR(100) NOT NULL,
    hotel_type VARCHAR(50) NOT NULL,
    address VARCHAR(255)
);

CREATE TABLE GUEST (
    guest_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    country VARCHAR(50)
);

CREATE TABLE ROOM (
    room_id INT PRIMARY KEY,
    room_type VARCHAR(50),
    capacity INT,
    base_price DECIMAL(10,2)
);

CREATE TABLE BOOKING (
    booking_id INT PRIMARY KEY,
    hotel_id INT,
    guest_id INT,
    arrival_date DATE,
    lead_time INT,
    is_canceled BOOLEAN,
    adr DECIMAL(10,2),
    FOREIGN KEY (hotel_id) REFERENCES HOTEL(hotel_id),
    FOREIGN KEY (guest_id) REFERENCES GUEST(guest_id)
);

CREATE TABLE BOOKING_ROOM (
    booking_id INT,
    room_id INT,
    price_at_booking DECIMAL(10,2),
    number_of_rooms INT,
    PRIMARY KEY (booking_id, room_id),
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id),
    FOREIGN KEY (room_id) REFERENCES ROOM(room_id)
);

CREATE TABLE STAY_DETAIL (
    booking_id INT PRIMARY KEY,
    weekend_nights INT,
    week_nights INT,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id)
);

CREATE TABLE Note (
    id INTEGER PRIMARY KEY,
    data VARCHAR(10000),
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User (id)
);

CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150) UNIQUE,
    password VARCHAR(150)
);

CREATE TABLE ProfileData (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(50),
    address_1 VARCHAR(100),
    address_2 VARCHAR(100),
    city VARCHAR(100),
    state CHAR(2),
    in_state_status BOOLEAN,
    zip_code VARCHAR(9),
    profile_completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE FuelOrderFormData (
    id INTEGER PRIMARY KEY,
    gallons INTEGER,
    delivery_date DATE,
    address_1 VARCHAR(100),
    address_2 VARCHAR(100),
    city VARCHAR(100),
    state CHAR(2),
    zip_code VARCHAR(9),
    in_state_status BOOLEAN,
    price FLOAT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User (id)
);

import sqlite3

conn = sqlite3.connect('Service_appointment.db')

cursor = conn.cursor()


# User Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        user_name TEXT
    )
    '''
)


# Service Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS service (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT,
        admin_id TEXT
    )
    '''
)


# Slot Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS slot(
        slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_date TEXT,
        slot_time TEXT,
        slot_status TEXT DEFAULT 'Available',
        service_id INTEGER
    )
    '''
)


# Appointment Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS appointment(
        app_id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_id INTEGER,
        user_id TEXT
    )
    '''
)


conn.commit()
conn.close()
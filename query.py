import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
bot_db = os.getenv('bot_db')

def connect_to_db():
    conn = sqlite3.connect(bot_db)
    cursor = conn.cursor()
    return conn, cursor


# Insert user
def insert_user(user_id, user_name):
    conn , cursor = connect_to_db()

    cursor.execute('INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?,?)', (user_id, user_name))

    conn.commit()
    conn.close()


# Show available services
def show_available_services():
    conn , cursor = connect_to_db()

    cursor.execute('SELECT service_id, service_name FROM service ')
    services = cursor.fetchall()

    conn.close()
    return services


# Get Date
def get_dates(service_id):
    conn , cursor = connect_to_db()

    cursor.execute('SELECT DISTINCT slot_date FROM slot WHERE service_id = ?',(service_id,))
    dates = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return dates


# Get Time
def get_times(service_id, date):
    conn, cursor = connect_to_db()

    cursor.execute(
        '''
        SELECT slot_id, slot_time FROM slot
        WHERE service_id = ? And slot_date = ? AND slot_status = 'Available'
        ORDER BY slot_time ASC
        ''', (service_id, date)
    )

    times = cursor.fetchall()

    conn.close()
    return times


# Book appointment
def book_appointment(user_id, slot_id):
    conn , cursor = connect_to_db()

    cursor.execute('INSERT INTO appointment (user_id, slot_id) VALUES (?,?)', (user_id, slot_id))

    conn.commit()
    conn.close()


# Update reserved appointments to booked
def update_slot_status(slot_id):
    conn, cursor = connect_to_db()

    cursor.execute('UPDATE slot SET slot_status = "booked" WHERE slot_id = ?', (slot_id,))

    conn.commit()
    conn.close()


# Insert Slot
def insert_slot(service_id, dates, times):
    conn, cursor = connect_to_db()

    for t in times:
        cursor.execute('INSERT INTO slot (service_id, slot_date, slot_time, slot_status) VALUES (?,?,?,?)', (service_id, dates, t, 'Available'))

    conn.commit()
    conn.close()

# Insert service
def insert_service(name, admin_id):
    conn, cursor = connect_to_db()

    cursor.execute('INSERT INTO service (service_name, admin_id) VALUES (?,?)', (name, admin_id))
    service_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return service_id

# Show booked appointments
def get_user_appointments(user_id):
    conn, cursor = connect_to_db()

    cursor.execute("""
        SELECT slot_date, slot_time, service_name FROM appointment
        JOIN slot ON appointment.slot_id = slot.slot_id
        JOIN service ON slot.service_id = service.service_id
        WHERE appointment.user_id = ?
        ORDER BY slot_date, slot_time
""", (user_id,))
    
    result = cursor.fetchall()

    conn.close()
    return result


def get_admin_appointments(admin_id):
    conn, cursor = connect_to_db()

    cursor.execute("""
        SELECT slot_date, slot_time, service_name, user_name FROM appointment
        JOIN slot ON appointment.slot_id = slot.slot_id
        JOIN service ON slot.service_id = service.service_id
        JOIN users ON appointment.user_id = users.user_id
        WHERE service.admin_id = ?
        ORDER BY slot_date, slot_time
""", (admin_id,))
    result = cursor.fetchall()
    
    conn.close()
    return result

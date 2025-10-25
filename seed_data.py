import sqlite3

# Connect to database
conn = sqlite3.connect('Service_appointment.db')
cursor = conn.cursor()

# insert user
cursor.executemany('''
    INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?,?)
''',[
    ('u001', 'Alice'),
    ('u002', 'Bob'),
    ('u003', 'Charlie'),
    ('100974126', 'Amir_bluex'),
])

# Insert sample service
cursor.executemany('''
    INSERT INTO service (service_name, admin_id) VALUES (?,?)
''', [
    ('Dental Cleaning', 'admin001'),
    ('Eye checkup', 'admin002'),
    ('Therapy Session', 'admin003'),

])


# Insert Sample slot
cursor.executemany('''
    INSERT INTO slot (slot_date, slot_time, slot_status, service_id) VALUES (?,?,?,?)
''', [
    ('2025-09-10', '09:00', 'Available', 1),
    ('2025-09-10', '10:00', 'Available', 1),
    ('2025-09-11', '11:00', 'Available', 2),
    ('2025-09-11', '12:00', 'booked', 2),
    ('2025-09-12', '14:00', 'Available', 3),
]) 

# Insert sample appointments
cursor.executemany('''
    INSERT INTO appointment (slot_id, user_id) VALUES(?,?)
''', [
    (4, 'u001'),
    (1, 'u002'),
    (3, '100974126')
])

conn.commit()
conn.close()

print('Database setup complete with sample data')
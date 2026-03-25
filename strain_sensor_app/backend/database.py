import sqlite3

DB = "patients.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        filename TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_patient(name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO patients (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_patients():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM patients")
    patients = c.fetchall()

    conn.close()
    return patients
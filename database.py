import sqlite3


def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    
    # ---------------- RESUMES TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_email TEXT,

    fullname TEXT,

    phone TEXT,

    address TEXT,

    college TEXT,

    degree TEXT,

    cgpa TEXT,

    skills TEXT,

    projects TEXT,

    certificates TEXT,

    objective TEXT

)
""")
# ---------------- INTERNSHIP TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS internships (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company TEXT,

    role TEXT,

    location TEXT,

    duration TEXT,

    skills TEXT

)
""")
# Add sample internships

cursor.execute("""
SELECT COUNT(*) FROM internships
""")

count = cursor.fetchone()[0]


if count == 0:

    cursor.execute("""
    INSERT INTO internships
    (company, role, location, duration, skills)

    VALUES

    ('Google','Data Science Intern','Remote','3 Months','Python, ML'),

    ('Microsoft','AI Intern','Remote','6 Months','Python, AI'),

    ('Infosys','Web Developer Intern','Bangalore','3 Months','HTML, CSS, Flask')

    """)


conn.commit()
conn.close()
# ---------------- APPLICATIONS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_email TEXT,

    internship_id INTEGER,

    applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")
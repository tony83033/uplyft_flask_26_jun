import sqlite3

conn = sqlite3.connect('contact_information.db')
query = (''' CREATE TABLE CONTACT_INFORMATION
            (NAME           INT    NOT NULL,
            ADDRESS        CHAR(50) NOT NULL,
            PHONE_NUMBER    INT,
            LAST_SEARCHED_DATE DATE );''')
conn.execute(query)
conn.close()
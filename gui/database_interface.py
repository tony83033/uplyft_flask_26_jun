import sqlite3
from pathlib import Path

import requests
import logging
import json
import datetime
from dateutil.parser import parse

logging.basicConfig(level=logging.INFO, filename='app5-lasd.log', filemode='w')
logger = logging.getLogger(__name__)


def insert_contact(age, race, booking_id, last_searched_date, range, web=False):
    if web:
        db_path = Path(Path.cwd()) / "gui" / "contact_information.db"
    else:
        db_path = "./contact_information.db"
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO CONTACT_INFORMATION (AGE,RACE,BOOKING_ID,LAST_SEARCHED_DATE, RANGE) \
VALUES (?,?,?,?,?)", (age, race, booking_id, last_searched_date, range))
    conn.commit()
    conn.close()


def inset_bail_amount(web=False, timeMin = 0):
    if web:
        db_path = Path(Path.cwd()) / "gui" / "contact_information.db"
    else:
        db_path = "./contact_information.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the query to retrieve rows where 'bail_value' is empty and 'last_fetched_at' is more than 15 minutes earlier
    current_time = datetime.datetime.now()
    time_threshold = current_time - datetime.timedelta(minutes=timeMin)
    cursor.execute(
        "SELECT BOOKING_ID, TOTAL_BAIL_AMOUNT, BAIL_DATA_LAST_FETCHED_AT FROM DATA_INFORMATION WHERE (TOTAL_BAIL_AMOUNT IS NULL OR TOTAL_BAIL_AMOUNT = '') AND (BAIL_DATA_LAST_FETCHED_AT < ? OR BAIL_DATA_LAST_FETCHED_AT IS NULL OR BAIL_DATA_LAST_FETCHED_AT = '')",
        (time_threshold,))

    # Fetch the first row
    rows = cursor.fetchall()
    for row in rows:
        BOOKING_ID, bail_value, last_fetched_at = row
        # Convert 'last_fetched_at' to a datetime object for comparison
        fetched_at_datetime = current_time
        if last_fetched_at is not None:
            fetched_at_datetime = parse(last_fetched_at)

        if fetched_at_datetime < time_threshold or last_fetched_at == None:

            url = "https://app5.lasd.org/iic/LoadCaseInfo"

            payload = f"draw=1&columns%5B0%5D%5Bdata%5D=FULL_BCA_CASE_NO&columns%5B0%5D%5Bname%5D=FULL_BCA_CASE_NO&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=BCA_CASE_NO&columns%5B1%5D%5Bname%5D=BCA_CASE_NO&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=COURT_NAME&columns%5B2%5D%5Bname%5D=COURT_NAME&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=COURT_ADDRESS&columns%5B3%5D%5Bname%5D=COURT_ADDRESS&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=COURT_CITY&columns%5B4%5D%5Bname%5D=COURT_CITY&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=BCA_BAIL_AMO1&columns%5B5%5D%5Bname%5D=BCA_BAIL_AMO1&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=BCA_TOT_FINE1&columns%5B6%5D%5Bname%5D=BCA_TOT_FINE1&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=BCA_NEXT_COURT_DATE_1&columns%5B7%5D%5Bname%5D=BCA_NEXT_COURT_DATE_1&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=BCA_DATE_OF_SENTENCE&columns%5B8%5D%5Bname%5D=BCA_DATE_OF_SENTENCE&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=BCH_LENGTH_OF_SENTENCE&columns%5B9%5D%5Bname%5D=BCH_LENGTH_OF_SENTENCE&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=BCA_DISP_CODE&columns%5B10%5D%5Bname%5D=BCA_DISP_CODE&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=FULL_BCA_CASE_NO&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=false&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=-1&search%5Bvalue%5D=&search%5Bregex%5D=false&bkgNum={str(BOOKING_ID)[1:]}"
            # payload = "draw=1&" \
            #           "columns%5B6%5D%5Bdata%5D=BCA_TOT_FINE1&" \
            #           "columns%5B6%5D%5Bname%5D=BCA_TOT_FINE1&" \
            #           "columns%5B6%5D%5Bsearchable%5D=true&" \
            #           "columns%5B6%5D%5Borderable%5D=true&" \
            #           "columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&" \
            #           "columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&"\
            #           f"bkgNum={str(BOOKING_ID)[1:]}"
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'ASP.NET_SessionId=d4li1v4rppamfstyt1jmzgrq; __RequestVerificationToken_L2lpYw2=LcdLFkTc5NcBc-kjF0DdkmsMMH8np5do4gfS3GlkT9Rmt316eOOxWQ5JMy8zXJRZrPvGKlS4JYDm8RoVKHT5nqyzPm6i_somBZVP8VCpFBU1; TS0117a92f=01fffec8367a24940a2df8c937dfdb5d664c27b400b45d68859d1cc4b294e9aea90ccf875bc3f349a5418664ef05914a8f99c80e43a5da3baf322bd7295ce5400ab0135406dd7f4110243e657c25d5125fc8216483; TS0117a92f=01fffec8364ec4ea7e81b5ebf889d0bce31456f0d9dc3fbe6dcde74eba37ff033cbc703415eaab79c15891e58f4a35314f7e4c3115c2a831a8cb076fe30bc27c70fac2c097b5a7d24acdef68f2dc75d6d4f8b396ff',
                'DNT': '1',
                'Origin': 'https://app5.lasd.org',
                'Referer': 'https://app5.lasd.org/iic/Details',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
            try:
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

                if response.status_code == 200:
                    # Process the JSON response
                    data = json.loads(response.text)["data"]
                    print(data)
                    bail_amount_sum = 0
                    for item in data:
                        bail_amount_sum += float(item["BCA_BAIL_AMO1"].replace(',', '').strip()) if item[
                            "BCA_BAIL_AMO1"].replace(',', '').replace('.', '').strip().isdigit() else 0

                    if data:
                        # Update the row with the fetched 'bail_value' and current timestamp in 'last_fetched_at' column
                        cursor.execute(
                            "UPDATE DATA_INFORMATION SET TOTAL_BAIL_AMOUNT = ?,BAIL_DATA_LAST_FETCHED_AT = ? WHERE BOOKING_ID = ?",
                            (bail_amount_sum,current_time, BOOKING_ID))
                        conn.commit()
                        print(f"Bail value fetched and stored for ID: {BOOKING_ID}")
                    else:
                        print(f"No bail value fetched for ID: {BOOKING_ID}")
                else:
                    print(f"Request failed for ID: {BOOKING_ID}")
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                print(e)
                logging.error(f"Failed to retrieve bail value for ID {BOOKING_ID}. Error: {e}")

        else:
            print(f"Last fetched time is not within the threshold for ID: {BOOKING_ID}")

    # Close the database connection
    cursor.close()
    conn.close()


def insert_data(booking_id, last_searched_date, full_name, date_of_birth, age, race, book_date, location, arrest_date,
                custody_status, web=False):
    if web:
        db_path = Path(Path.cwd()) / "gui" / "contact_information.db"
    else:
        db_path = "./contact_information.db"
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO DATA_INFORMATION (LAST_SEARCHED_DATE, FULL_NAME, DATE_OF_BIRTH, AGE,RACE,BOOK_DATE, LOCATION, BOOKING_ID, ARREST_DATE, CUSTODY_STATUS) \
VALUES (?,?,?,?,?,?,?,?,?,?)", (
        last_searched_date, full_name, date_of_birth, age, race, book_date, location, booking_id, arrest_date,
        custody_status))
    conn.commit()
    conn.close()


def delete_data():
    conn = sqlite3.connect(Path(Path.cwd()) / "gui" / "contact_information.db")
    conn.execute("DELETE from DATA_INFORMATION")
    conn.commit()
    conn.close()


def delete_history(web=False):
    if web:
        db_path = Path(Path.cwd()) / "gui" / "contact_information.db"
    else:
        db_path = "./contact_information.db"
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE from CONTACT_INFORMATION")
    conn.commit()
    conn.close()


# def delete_contact_by_name(name):
#     conn = sqlite3.connect('contact_information.db')
#     conn.execute("DELETE from CONTACT_INFORMATION where name = ?",(name,))
#     conn.close()

# def edit_address_by_name(name, address):
#     conn = sqlite3.connect('contact_information.db')
#     conn.execute("UPDATE CONTACT_INFORMATION set ADDRESS = ? where NAME = ?", (name, address))
#     conn.commit()
#     conn.close()

# def edit_phone_number_by_name(name, phone_number):
#     conn = sqlite3.connect('contact_information.db')
#     conn.execute("UPDATE CONTACT_INFORMATION set ADDRESS = ? where NAME = ?", (name, phone_number))
#     conn.close()

def retrieve_contacts(web=False):
    results = []
    if web:
        db_path = Path(Path.cwd()) / "gui" / "contact_information.db"
    else:
        db_path = "./contact_information.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT * from CONTACT_INFORMATION")
    # Contact records are tuples and need to be converted into an array
    for row in cursor:
        results.append(list(row))

    conn.close()
    return results


def retrieve_data(last_searched_date):
    results = []
    conn = sqlite3.connect(Path(Path.cwd()) / "gui" / "contact_information.db")
    cursor = conn.execute(
        "SELECT  FULL_NAME, DATE_OF_BIRTH, AGE, RACE, BOOK_DATE, LOCATION, BOOKING_ID, ARREST_DATE, CUSTODY_STATUS, TOTAL_BAIL_AMOUNT from DATA_INFORMATION where LAST_SEARCHED_DATE = ?",
        (last_searched_date,))
    # Contact records are tuples and need to be converted into an array
    for row in cursor:
        results.append(list(row))
    # print(results)
    return results

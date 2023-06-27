import sqlite3
import datetime
from pathlib import Path
#

# # Connect to the SQLite database
db_path = Path(Path.cwd()) / "apps" / "db.sqlite3"
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
#
# # Get the current time
# current_time = datetime.datetime.now()
# # Insert a new row with 'id' and 'last_fetched_at' containing the current time
# booking_id = 6623951
# for i in range(20):
#     booking_id += 1
#     cursor.execute("INSERT INTO bail_record (id, last_fetched_at) VALUES (?, ?)", (booking_id, current_time))
#
# # Commit the changes
# conn.commit()
#
# # Close the database connection
# cursor.close()
# conn.close()
#
import sqlite3
import requests
import logging
import json
import datetime
from dateutil.parser import parse
logging.basicConfig(level=logging.INFO, filename='application.log', filemode='w')
logger = logging.getLogger(__name__)
# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute the query to retrieve rows where 'bail_value' is empty and 'last_fetched_at' is more than 15 minutes earlier
current_time = datetime.datetime.now()
time_threshold = current_time - datetime.timedelta(minutes=0)
cursor.execute("SELECT id, bail_value, last_fetched_at FROM bail_record WHERE (bail_value IS NULL OR bail_value = '') AND (last_fetched_at < ? OR last_fetched_at IS NULL OR last_fetched_at = '')", (time_threshold,))


# Fetch the first row
rows = cursor.fetchall()
for row in rows:
    id_value, bail_value, last_fetched_at = row
    # Convert 'last_fetched_at' to a datetime object for comparison
    fetched_at_datetime = parse(last_fetched_at)

    if fetched_at_datetime < time_threshold:

        url = "https://app5.lasd.org/iic/LoadCaseInfo"

        payload = f"draw=1&columns%5B0%5D%5Bdata%5D=FULL_BCA_CASE_NO&columns%5B0%5D%5Bname%5D=FULL_BCA_CASE_NO&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=BCA_CASE_NO&columns%5B1%5D%5Bname%5D=BCA_CASE_NO&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=COURT_NAME&columns%5B2%5D%5Bname%5D=COURT_NAME&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=COURT_ADDRESS&columns%5B3%5D%5Bname%5D=COURT_ADDRESS&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=COURT_CITY&columns%5B4%5D%5Bname%5D=COURT_CITY&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=BCA_BAIL_AMO1&columns%5B5%5D%5Bname%5D=BCA_BAIL_AMO1&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=BCA_TOT_FINE1&columns%5B6%5D%5Bname%5D=BCA_TOT_FINE1&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=BCA_NEXT_COURT_DATE_1&columns%5B7%5D%5Bname%5D=BCA_NEXT_COURT_DATE_1&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=BCA_DATE_OF_SENTENCE&columns%5B8%5D%5Bname%5D=BCA_DATE_OF_SENTENCE&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=BCH_LENGTH_OF_SENTENCE&columns%5B9%5D%5Bname%5D=BCH_LENGTH_OF_SENTENCE&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=BCA_DISP_CODE&columns%5B10%5D%5Bname%5D=BCA_DISP_CODE&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=FULL_BCA_CASE_NO&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=false&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=-1&search%5Bvalue%5D=&search%5Bregex%5D=false&bkgNum={id_value}"
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
                bail_amount_sum = 0
                for item in data:
                    bail_amount_sum += float(item["BCA_BAIL_AMO1"].replace(',', '').strip()) if item[
                        "BCA_BAIL_AMO1"].replace(',', '').replace('.', '').strip().isdigit() else 0

                if data:
                    # Update the row with the fetched 'bail_value' and current timestamp in 'last_fetched_at' column
                    cursor.execute("UPDATE bail_record SET bail_value = ? WHERE id = ?",
                                   (bail_amount_sum, id_value))
                    conn.commit()
                    print(f"Bail value fetched and stored for ID: {id_value}")
                else:
                    print(f"No bail value fetched for ID: {id_value}")
            else:
                print(f"Request failed for ID: {id_value}")
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(e)
            logging.error(f"Failed to retrieve bail value for ID {id_value}. Error: {e}")

    else:
        print(f"Last fetched time is not within the threshold for ID: {id_value}")

# Close the database connection
cursor.close()
conn.close()


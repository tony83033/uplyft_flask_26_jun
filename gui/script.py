from datetime import datetime
import os
import csv
import time
import argparse
import requests
import urllib3
import json
from gui.database_interface import insert_data, delete_history, inset_bail_amount
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from dateutil import parser

OUT_PERSON_DATA_FILE = time.strftime('%B%d%H%M.csv')

HEADER = {
    'authority': 'vinelink-mobile.vineapps.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'origin': 'https://vinelink.vineapps.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87'
                  ' Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'x-vine-application': 'VINELINK',
    # 'expires': 'Sat, 01 Jan 2000 00:00:00 GMT',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',

    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en;q=0.9,en-US;q=0.8',
}
MONTHS = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'sept': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
}


def get_formatted_date(date_text, age):
    # Mar 02, 1973
    if '*' in date_text:
        month = MONTHS[str(date_text.split()[0]).lower()]
        day = 1
        year = int(datetime.now().strftime("%Y"))-age
        return datetime.now().replace(year, month, day).strftime("%m/%d/%Y")
    else:
        date_text = date_text.lower()
        month, day, year = date_text.split(' ')
        month = int(MONTHS[month])
        day = int(day.strip(','))
        return '{:02}/{:02}/{}'.format(month, day, year)


def write_data(fname, data):
    # print("Write Data",fname,data)
    if not data:
        return
    if type(data) != list:
        data = [data]
    write_header = not os.path.isfile(fname)
    with open(fname, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if write_header:
            csv_writer.writeheader()
        csv_writer.writerows(data)


def _get_person_info(person_id, second_person_id):
    d = {}
    header = HEADER.copy()
    header['referer'] = 'https://vinelink.vineapps.com/search/persons;limit=20;offset=0;showPhotos=false;' \
                        'isPartialSearch=false;siteRefId=CASWVINE;personContextRefId=' + \
        str(person_id)
    params = (
        ('addImageWatermark', 'true'),
        ('includeRegistrantInfo', 'true'),
        ('includeCustomDisplayInfo', 'true'),
        ('includeChargeInfo', 'true'),
    )
    # https://vinelink-mobile.vineapps.com/api/v1/guest/persons/offenders/8298823?addImageWatermark=true&includeRegistrantInfo=true&includeCustomDisplayInfo=true&includeChargeInfo=true
    response = requests.get(
        'https://vinelink-mobile.vineapps.com/api/v1/guest/persons/offenders/' +
        str(second_person_id),
        headers=header, params=params, verify=False
    )
    try:
        data = response.json()
        # print(data)
        try:
            d['Book Date'] = data['offenderInfo']['bookedDate']
        except KeyError:
            d['Book Date'] = ''

        try:
            for location in data['locations']:
                if location['locationId'] != 507:
                    d['Location'] = location['locationName']
                    break
            else:
                d['Location'] = ''
        except KeyError:
            d['Location'] = ''
    except ValueError:
        pass

    return d


def get_person_info(person_id):
    # 5796288
    out_list = []
    params = (
        ('limit', '20'),
        ('offset', '0'),
        ('showPhotos', 'false'),
        ('isPartialSearch', 'false'),
        ('siteRefId', 'CASWVINE'),
        ('personContextRefId', str(person_id)),
        ('includeJuveniles', 'false'),
        ('includeSearchBlocked', 'false'),
        ('includeRegistrantInfo', 'true'),
        ('addImageWatermark', 'true'),
        ('personContextTypes', ['OFFENDER', 'DEFENDANT']),
    )
    header = HEADER.copy()
    header['referer'] = 'https://vinelink.vineapps.com/search/persons;limit=20;offset=0;showPhotos=false;' \
                        'isPartialSearch=false;siteRefId=CASWVINE;personContextRefId=' + \
        str(person_id)

    response = requests.get('https://vinelink-mobile.vineapps.com/api/v1/guest/persons', headers=header, params=params,
                            verify=False)

    # debugging purpose
    print("my response code", response.status_code)
    print("responsetext", response.text)
    # print(response.json(),person_id)
    # exit()
    try:
        # json module used here only json was not working
        person_data = json.loads(response.text)

        # print(person_data)
        for person in person_data['_embedded']['persons']:

            d = {'Booking ID': person_id}

            try:
                d['Full Name'] = ' '.join(
                    person['personName'].values()).strip()
            except KeyError:
                d['Full Name'] = ''
            try:
                d['Date of Birth'] = get_formatted_date(
                    person['dateOfBirth'], person['age'])
            except KeyError:
                d['Date of Birth'] = ''
            try:
                d['Custody Status'] = person['offenderInfo']['custodyStatus']['name']
            except KeyError:
                d['DCustody Status'] = ''
            try:
                d['Age'] = person['age']
            except KeyError:
                d['Age'] = ''
            try:
                d['Gender'] = person['gender']['name']
            except KeyError:
                d['Gender'] = ''
            try:
                d['Race'] = person['race']['name']
            except KeyError:
                d['Race'] = ''

            # Custody Status Date
            try:
                d['Custody Status Date'] = person['offenderInfo']['custodyStatusDate']
            except KeyError:
                d['Custody Status Date'] = ''
            second_person_id = person['personContext']['contextId']
            d.update(_get_person_info(person_id, second_person_id))
            out_list.append(d)

    except (ValueError, KeyError):
        pass
    return out_list


def print_or_sock(sock, message):
    if sock is not None:
        sock.send(message)
    else:
        print(message, sep="\n")


def start(context_id, npages, race=None,  range_lower=None, range_high=None, last_searched_date=None, sock=None):
    print(sock)

    for n in range(npages):
        _id = int(context_id) + n
        if context_id.startswith('0'):
            _id = '0' + str(_id)
        print_or_sock(sock, f"Sending Request for Id : {_id}")
        person_info = get_person_info(_id)
        # print(len(person_info),_id)
        # print(person_info)

        if not person_info:
            print_or_sock(sock, f'No Data Found for Id : {_id}',)
            continue
        print_or_sock(sock, f"Data Received for Id : {_id}")
        # string = ','.join(str(x) for x in person_info)
        for i in range(0, len(person_info)):
            # print(person_info)
            booking_id = person_info[i]['Booking ID']
            full_name = person_info[i]['Full Name']
            if not full_name:
                full_name = "No data"
            date_of_birth = person_info[i]['Date of Birth']
            if not date_of_birth:
                date_of_birth = "No data"
            age = person_info[i]['Age']
            if not age:
                age = "No data"
            race1 = person_info[i]['Race']
            if not race1:
                race1 = "No data"
            book_date = person_info[i]['Book Date']
            if not book_date:
                book_date = "No data"
            location = person_info[i]['Location']
            if not location:
                location = "No data"
            arrest_date = person_info[i]['Custody Status Date']
            if not arrest_date:
                arrest_date = "No data"
            custody_status = person_info[i]['Custody Status']
            if not custody_status:
                custody_status = "No data"
        for person in person_info:
            # failure case only race is provided
            if race == 'all' and range_lower == 20 and range_high == 70:
                # for debugging
                print("failure case")
                write_data(OUT_PERSON_DATA_FILE, person)
                insert_data(booking_id, last_searched_date, full_name, date_of_birth,
                            age,     race1, book_date, location, arrest_date, custody_status, True)


            # age range  case when only age filter is provided
            elif race == 'all' and range_lower <= person['Age'] <= range_high:

                print("age range case only")
                write_data(OUT_PERSON_DATA_FILE, person)
                insert_data(booking_id, last_searched_date, full_name, date_of_birth,
                            age, race1, book_date, location, arrest_date, custody_status, True)
            # success case when race is provided only or if race is provided with  age range filter
            elif race.upper() == person['Race'].upper() and range_lower <= person['Age'] <= range_high:

                #  for debugging
                print("success")

                write_data(OUT_PERSON_DATA_FILE, person)
                insert_data(booking_id, last_searched_date, full_name, date_of_birth,
                            age, race1, book_date, location, arrest_date, custody_status, True)
            inset_bail_amount(web=True)
    print_or_sock(sock, f"Done !")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraping Jail Database')
    parser.add_argument('context_id', metavar='ID',
                        type=str, nargs=1, help='Context ID')
    parser.add_argument('npages', metavar='Pages', type=int,
                        nargs=1, help='Number of pages')
    parser.add_argument('--race', type=str, help='Race')
    parser.add_argument('--age', type=str, help='Age range (like 20-50)')
    args = parser.parse_args()

    if args.age:
        r_low, r_high = map(int, args.age.split('-'))
    else:
        r_low = None
        r_high = None

    start(args.context_id[0], args.npages[0], args.race, r_low, r_high)
    print("scraping session is done")

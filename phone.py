from twilio.rest import Client
from bs4 import BeautifulSoup
import requests
import re
import datetime
import time
import googleapi
import dateutil.parser as dp
import json

with open('web_cred.txt', 'r') as f:
    accountSID = f.readline().rstrip()
    authToken = f.readline().rstrip()

client = Client(accountSID, authToken)


myTwilioNumber = '+xxxxxxx'

PhoneList = {'David': '+xxxxxxx', 'Kjirsten': '+xxxxxxx'}


def send_txt():
    with open('data.json',) as f:
        data = json.load(f)
    divider = "*" * 32
    date, url, photo_id = googleapi.get_photos()
    quote = get_quote()
    parsed_t = dp.parse(date)
    form_date = parsed_t.strftime('%D')
    today_date = datetime.datetime.now().date().strftime('%D')
    for person in data['Phone'].keys():
        client.messages.create(body=f'Hi {person}, Brody Here! This photo was taken on {form_date}.\n{divider}\nThis '
                                    f'photo needs a name! Please respond with one.\n{divider}\nThe quote of the day is '
                                    f'({today_date}):\n{quote}', media_url=url, from_=myTwilioNumber,
                               to=data['Phone'][person])
    # update list
    new_entry = ['None', date, photo_id]
    with open('data.json',) as f:
        data = json.load(f)
    try:
        data['Photos'].append(new_entry)
    except:
        data['Photos'] = new_entry
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_quote():
    r = requests.get('https://www.brainyquote.com/quote_of_the_day')
    soup = BeautifulSoup(r.text, features='html.parser')
    tags = soup.findAll('a', attrs={'class': 'oncl_q'})
    all_content = str(tags[0].contents)
    quote = re.findall(r'"(.*?)"', all_content)
    return quote[0]


def run_time():
    time_day = 60 * 60 * 12
    time_hour = 60 * 30
    while 1 == 1:
        if datetime.datetime.now().time() > datetime.time(hour=9):
            send_txt()
            print('Text sent at: ' + datetime.datetime.now().time().strftime('%T'))
            time.sleep(time_day)
        else:
            print('Tested at: ' + datetime.datetime.now().time().strftime('%T'))
            client.messages.create(body='Tested at: ' + datetime.datetime.now().time().strftime('%T'),
                                   from_=myTwilioNumber, to=PhoneList['David'])
            time.sleep(time_hour)


run_time()






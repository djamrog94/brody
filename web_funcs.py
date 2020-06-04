import json
from twilio.rest import Client
from random import randint
import dateutil.parser as dp
from googleapi import get_specific

with open('web_cred.txt', 'r') as f:
    accountSID = f.readline().rstrip()
    authToken = f.readline().rstrip()

client = Client(accountSID, authToken)


myTwilioNumber = '+17158008105'


def convert_to_person(from_number):
    with open('data.json',) as f:
        data = json.load(f)
    for person in data['Phone'].keys():
        if data['Phone'][person] == from_number:
            return person


def convert_to_number(from_person):
    with open('data.json',) as f:
        data = json.load(f)
    for person in data['Phone'].keys():
        if person.lower() == from_person.lower():
            return data['Phone'][person]


def update_title(incoming_msg, from_person):
    with open('data.json',) as f:
        data = json.load(f)
    try:
        if data['Photos'][-1][0] == 'None':
            data['Photos'][-1][0] = incoming_msg.rstrip().title()
            data['Photos'][-1].append(convert_to_person(from_person))
            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)
            client.messages.create(body=f'Name updated to {incoming_msg.title()}', from_=myTwilioNumber, to=from_person)
        else:
            descrip = data['Photos'][-1][0]
            updated = data['Photos'][-1][3]
            client.messages.create(body=f'Name has already been updated to: {descrip}, by {updated}.',
                                   from_=myTwilioNumber, to=from_person)
    except:
        print('Error updating name')


def get_photo():
    with open('data.json',) as f:
        data = json.load(f)
    rand_index = randint(0, len(data['Photos']) - 1)
    # history = open("history.txt", "r")
    # history_db = history.read()
    # history = open("history.txt", "a+")
    # while str(rand_index) in history_db:
    #     rand_index = randint(0, len(data['Photos']) - 1)
    # history.write(str(rand_index)+'\n')
    # history.close()
    return data['Photos'][rand_index][0], data['Photos'][rand_index][1], data['Photos'][rand_index][2]


def send_message(incoming_msg, from_number):
    with open('data.json',) as f:
        data = json.load(f)
    divider = "*" * 32
    try:
        to_person = incoming_msg.split(";", 1)[0].split('send ')[1].title()
    except:
        to_person = incoming_msg.split(";", 1)[0].split('Send ')[1].title()
    to_number = convert_to_number(to_person)
    try:
        message = incoming_msg.split(";", 1)[1].split('message ')[1]
    except:
        message = incoming_msg.split(";", 1)[1].split('Message ')[1]
    description, date, photo_id = get_photo()
    url = get_specific(photo_id)
    parsed_t = dp.parse(date)
    form_date = parsed_t.strftime('%D')
    if to_person in data['Phone'].keys():
        client.messages.create(body=f'Hello {to_person}! {convert_to_person(from_number)} wanted to say: {message}\n'
                                    f'{divider}\nThis is a random pic of Brody. Taken on {form_date},'
                                    f' it is called: {description}.', media_url=url, from_=myTwilioNumber,
                               to=to_number)
        client.messages.create(body=f'Message was succesfully sent to {to_person}; saying: {message}.',
                               from_=myTwilioNumber, to=from_number)
    else:
        client.messages.create(body='That person is not in the phonebook, please try again.',
                               from_=myTwilioNumber, to=from_number)



from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import requests
from bs4 import BeautifulSoup
import json
import sys
import webbrowser
from dateutil.tz import gettz

import google.oauth2.credentials
import google_auth_oauthlib.flow

# list of classes
classes = [
    "Český jazyk",
    "Český jazyk a literatura",
    "Anglický jazyk",
    "Německý jazyk",
    "Francouzský jazyk",
    "Ruský jazyk",
    "Občanská nauka",
    "Základy společenských věd",
    "Dějepis",
    "Matematika",
    "Fyzika",
    "Fyzikální praktika",
    "Biologie",
    "Biologická praktika",
    "Chemie",
    "Chemická praktika",
    "Zeměpis",
    "Zeměpisná praktika",
    "Přírodovědná praktika",
    "Informatika a výpočetní technika",
    "Hudební výchova",
    "Výtvarná výchova",
    "Tělesná výchova",

    "Globální výchova",
    "Vlastivědný seminář",
    "Matematika s podporou ICT",
    "Školní časopis",
    "Literární praktikum",
    
    "Psaní na PC",
    "Geometrické praktikum",
    
    "Matematický seminář",
    "Chemický seminář",
    "Biologický seminář",
    "Fyzikální seminář",
    "Deskriptivní geometrie",
    "Zeměpisný seminář",
    "Dějepisný seminář",
    "Společenskovědní seminář",
    "Sociologie a psychologie",
    "Politologie a mezinárodní vztahy",
    "Ekonomika podnikání",
    "Konverzace z angličtiny",
    "Konverzace z francouzštiny",
    "Konverzace z němčiny",
    "Aplikace Windows a programování",

    "Literální seminář",
    "Chemicko-biologická praktika",
    "Biologie člověka a výchova ke zdraví",
    "Konverzace z ruštiny",
    "Fyzika pro lékařské fakulty",
]

   
# add classes to the calendar
def addCalendar(predmet, start, end, room, about, creds):
    # create the credentials
    credentials = google.oauth2.credentials.Credentials(
        creds["token"],
        refresh_token = creds["refresh_token"],
        token_uri = creds["token_uri"],
        client_id = creds["client_id"],
        client_secret = creds["client_secret"],
        scopes = creds["scopes"])
    # contact the calendar
    CAL = build('calendar', 'v3', credentials=credentials)
    # check for daylight savings
    time = datetime.datetime.now(gettz("Europe/Prague")).isoformat().split("+")[1]
    tz = "UTC+1"
    if time == "02:00":
        tz = "UTC+2"
    # create the event
    EVENT = {
        'summary': f"{predmet}",
        'start': {f'dateTime': f'{start}', "timeZone": f"{tz}"},
        'end': {'dateTime': f'{end}', "timeZone": f"{tz}"},
        'location': f'{room}',
        'description': f'{about}',
    }
    # insert the event into the calendar
    e = CAL.events().insert(calendarId='primary', body=EVENT).execute()
    


def getTimeTable(Name, Sem, creds):
    # get the timetable
    r = requests.get(f"https://gym-nymburk.bakalari.cz/bakaweb/Timetable/public/Actual/Class/{ Name }")
    soup = BeautifulSoup(r.text, "html.parser")
    finder = soup.find_all('div', attrs={"class":'day-item-hover'})
    # delete previous calendar entries from the website that are in the future
    delete(creds)
    # loop through every class
    for x in finder:
        data_detail = x['data-detail'].replace('null', '"Nothing"')
        data_detail = eval(data_detail)
        # set each attribute to the right variable
        subjecttext = data_detail['subjecttext']
        try:
            teacher = data_detail['teacher']
            room = data_detail['room']
            if room == "mim" or room == "A" or room == 'T' or room == 'DisV':
                room = str(room)
            else:
                room = int(room)
        except:
            if data_detail['type'] == 'absent':
                teacher = ""
                room = "Volno"
                subjecttext = "Neni hodina | " + subjecttext
            else:
                continue
        try:
            jaz = data_detail["group"]
        except:
            jaz = ''
        if jaz not in Sem:
            continue
        # divide the subject and time
        splited = subjecttext.split(' |')
        predmet = splited[0]
        date = splited[1]
        try:
            time = splited[2]
        except:
            # if the class is not there, skip
            continue
        # create the right time format
        date = date.replace('po', '')
        date = date.replace('út', '')
        date = date.replace('st', '')
        date = date.replace('čt', '')
        date = date.replace('pá', '')
        date = date.replace(' ', '')
        t = 0
        while t < 10:
            time = time.replace(")", "")
            time = time.replace(" ", '')
            time = time.replace(f'{t}(', '')
            t = t+1
        start = time.split('-')[0]+":00"
        end = time.split('-')[1]+":00"

        date = date.split('.')
        date = str(datetime.datetime.today().year) + '-'+date[1]+'-'+date[0]
        start = date + "T" + start
        end = date + "T" + end
        start = start.split("T")
        if start[1].startswith("1") == False:
            start = start[0] + "T" + '0' + start[1]
        else:
            start = start[0] + "T" + start[1]
        end = end.split("T")
        if end[1].startswith("1") == False:
            end = end[0] + "T" + '0' + end[1]
        else:
            end = end[0] + "T" + end[1]

        # skip past classes
        if type(room) == int:
            room = "Učebna " + str(room)
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        now = now.isoformat()
        now = now.split('.')[0]
        now = now.split("T")
        datenow = now[0]
        timenow = now[1]
        if timenow.startswith('0') == True:
            timenow = timenow[0:]
        now = datenow+'T'+timenow
        if now > start:
            print(predmet, start, "SKIPPED")
            continue

        addCalendar(predmet, start, end, room, teacher, creds)
        print(predmet, room, teacher, start) # start, end,


# delete previous calendar entries from the website that are in the future
def delete(creds):
    # get and create credentials
    credentials = google.oauth2.credentials.Credentials(
        creds["token"],
        refresh_token = creds["refresh_token"],
        token_uri = creds["token_uri"],
        client_id = creds["client_id"],
        client_secret = creds["client_secret"],
        scopes = creds["scopes"])
    # connect to the calendar
    CAL = build('calendar', 'v3', credentials=credentials)
    now = datetime.datetime.now().isoformat()
    now = now.split('.')[0] + 'Z'
    # get the list of all events in the calendar
    e = CAL.events().list(calendarId='primary', timeMin=now).execute()
    items = e['items']
    # delete the events
    for z in items:
        if z['status'] == 'confirmed':
            if z['summary'] in classes:
                print('deleted' + ' '+ z['summary'])
                eventid = z['id']
                event = CAL.events().delete(calendarId='primary', eventId=eventid).execute()
            else:
                continue
        else:
            continue



#if __name__ == "__main__":
   #getTimeTable("ZK", ['aj5', 'nej2', 'fys1', 'mas2', 'eps3', ''], '') #the '' has to be there, in order for it to work, jaz = ' '

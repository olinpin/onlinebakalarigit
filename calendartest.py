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
#$oauth_callback = 'https://accounts.google.com/o/oauth2/auth?client_id=669046485288-hk0o6915jn4givcqe1bfiso29i7fle67.apps.googleusercontent.com&redirect_uri=https:%2f%2fbakalaricz.herokuapp.com%2Frozvrh%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&access_type=offline&response_type=code'

def authorization():
    try:
        import argparse
        #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        flags = tools.argparser.parse_args([])
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    #webbrowser.open(oauth_callback)
    print('opened')
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)          
    

def addCalendar(predmet, start, end, room, about):
    authorization()
    store = file.Storage('storage.json')
    creds = store.get()
    CAL = build('calendar', 'v3', http=creds.authorize(Http()))
    GMT_OFF = "-01:00"
    EVENT = {
        'summary': f"{predmet}",
        'start': {f'dateTime': f'{start}', "timeZone": "UTC+2"},
        'end': {'dateTime': f'{end}', "timeZone": "UTC+2"},
        'location': f'{room}',
        'description': f'{about}',
    }

    e = CAL.events().insert(calendarId='primary', body=EVENT).execute()
    


def getTimeTable(Name, Sem):
    print(Name)
    r = requests.get(f"https://gym-nymburk.bakalari.cz/bakaweb/Timetable/public/Actual/Class/{ Name }")
    soup = BeautifulSoup(r.text, "html.parser")
    finder = soup.find_all('div', attrs={"class":'day-item-hover'})
    delete()
    for x in finder:
        data_detail = x['data-detail'].replace('null', '"Nothing"')
        data_detail = eval(data_detail)
        subjecttext = data_detail['subjecttext']
        try:
            teacher = data_detail['teacher']
            room = data_detail['room']
            if room == "mim" or room == "A" or room == 'T' or room == 'DisV':
                room = str(room)
            else:
                room = int(room)
        except:
            continue

        try:
            jaz = data_detail["group"]
        except:
            jaz = ''
        if jaz not in Sem:
            continue
        splited = subjecttext.split(' |')
        predmet = splited[0]
        date = splited[1]
        try:
            time = splited[2]
        except:
            predmet = "ODPADLÁ HODINA"
            time = splited[1]
            date = splited[0]
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

        
        if type(room) == int:
            room = "Učebna " + str(room)
        now = datetime.datetime.now().isoformat()
        now = now.split('.')[0]
        now = now.split("T")
        datenow = now[0]
        timenow = now[1]
        if timenow.startswith('0') == True:
            timenow = timenow[0:]
        now = datenow+'T'+timenow
        if now > start:
            print(predmet, "SKIPPED")
            continue

        addCalendar(predmet, start, end, room, teacher)
        print(predmet, room, teacher, start) # start, end,
    open('storage.json', 'r+').truncate()


def delete():
    authorization()
    store = file.Storage('storage.json')
    creds = store.get()
    CAL = build('calendar', 'v3', http=creds.authorize(Http()))
    now = datetime.datetime.now().isoformat()
    now = now.split('.')[0] + 'Z'
    e = CAL.events().list(calendarId='primary', timeMin='2020-10-14T11:35:00Z').execute()
    items = e['items']
    
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
   #getTimeTable("ZK", ['aj5', 'nej2', 'fys1', 'mas2', 'eps3', ''])#the ' ' has to be there, in order for it to work, jaz = ' '

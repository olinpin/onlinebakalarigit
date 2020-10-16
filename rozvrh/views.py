from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from oauth2client import file, client, tools


from .Calendartest.calendartest import * # import getTimeTable, addCalendar, delete


import google.oauth2.credentials
import google_auth_oauthlib.flow



classes = [
    ("ZP","1A"),
    ("ZQ","1PA"),
    ("ZR","1PB"),
    ("ZL","2A"),
    ("ZM","2SA"),
    ("ZN","2SB"),
    ("ZK","3A"),
    ("ZI","3TA"),
    ("ZJ","3TB"),
    ("ZG","4A"),
    ("ZE","4KA"),
    ("ZF","4KB"),
    ("ZC","5QA"),
    ("ZD","5QB"),
    ("Z9","6XA"),
    ("ZA","6XB"),
    ("Z6","7MA"),
    ("Z7","7MB"),
    ("Z3","8OA"),
    ("Z4","8OB")
]
aj = [
    ("aj1", "aj1"),
    ("aj2", "aj2"),
    ("aj3", "aj3"),
    ("aj4", "aj4"),
    ("aj5", "aj5"),
    ("aj6", "aj6"),
]
jazyk = [
    (" ", "Žádný"),
    ("nej1", "nej1"),
    ("nej2", "nej2"),
    ("nej3", "nej3"),
    ("frj1", "frj1"),
    ("frj2", "frj2"),
    ("frj3", "frj3"),
    ("ruj", "ruj"),
]
Sem1 = [
    (" ", "Žádný"),
    ("zes1", "zes1"),
    ("chs1", "chs1"),
    ("fys1", "fys1"),
    ("sps1", "sps1"),
    ("bi1A", "bi1A"),
    ("des1", "des1"),
    ("eps1", "eps1"),
]
Sem2 = [
    (" ", "Žádný"),
    ("svs2", "svs2"),
    ("fys2", "fys2"),
    ("mas2", "mas2"),
    ("sps2", "sps2"),
    ("eps2", "eps2"),
    ("bis2", "bis2"),
    ("aw2", "aw2"),
]
Sem3 = [
    (" ", "Žádný"),
    ("chs3", "chs3"),
    ("ps2", "ps2"),
    ("mas3", "mas3"),
    ("sps3", "sps3"),
    ("eps3", "eps3"),
    ("kaz3", "kaz3"),
]
skupina = [
    (" ", "Žádná"),
    ("SkA", "SkA"),
    ("SkB", "SkB"),
]
gender = [
    (" ", "Žádný"),
    ("Chl", "Chlapec"),
    ("Dív", "Dívka"),
]


# Create your views here.
class RozvrhForm(forms.Form):
    trida = forms.ChoiceField(choices=classes, label="Třída")
    aj = forms.ChoiceField(choices=aj, label="Jazyková skupina")
    jazyk2 = forms.ChoiceField(choices=jazyk, label="Cizí jazyková skupina")
    Sem1 = forms.ChoiceField(choices=Sem1, label="První seminář")
    Sem2 = forms.ChoiceField(choices=Sem2, label="Druhý seminář")
    Sem3 = forms.ChoiceField(choices=Sem3, label="Třetí seminář")
    skupina = forms.ChoiceField(choices=skupina, label="Skupina")
    gender = forms.ChoiceField(choices=gender, label="Pohlaví")


def index(request):
    if request.method == 'POST':
        form = RozvrhForm(request.POST)
        if form.is_valid():
            trida = form.cleaned_data['trida']
            aj = form.cleaned_data['aj']
            jazyk2 = form.cleaned_data['jazyk2']
            Sem1 = form.cleaned_data['Sem1']
            Sem2 = form.cleaned_data['Sem2']
            Sem3 = form.cleaned_data['Sem3']
            skupina = form.cleaned_data['skupina']
            gender = form.cleaned_data["gender"]
            PList = [aj, jazyk2, Sem1, Sem2, Sem3, skupina, gender, '']
            request.session['trida'] = trida
            request.session['PList'] = PList
        print(request.session['PList'])
        if 'creds' not in request.session:
            SCOPES = 'https://www.googleapis.com/auth/calendar'
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', SCOPES)
            flow.redirect_uri = 'https://bakalaricz.herokuapp.com/rozvrh/form'
            authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes="true")
            request.session['state'] = state
            return HttpResponseRedirect(authorization_url)
        else:
            return redirect('/form')
    
    return render(request, "rozvrh/index.html", {
        "form": RozvrhForm(), 
        'worked': ""
    })
def rozvrhAdd(request):
    print(request)
    PList = request.session['PList']
    trida = request.session['trida']
    state = request.session['state']
    authorization_response = request.build_absolute_uri()
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', SCOPES)
    flow.fetch_token(authorization_response=authorization_response)
    flow.redirect_uri = 'https://bakalaricz.herokuapp.com/rozvrh/form'
    creds = flow.credentials
    request.session['creds'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    #getTimeTable(trida, PList, request.session['creds'])
    print('Im working')
    return render(request, "rozvrh/rozvrh.html")

def greet(request, name):
    return render(request, "rozvrh/greet.html", {
        'name': name.capitalize()
    })                               

def PrivacyPolicy(request):
    return render(request, "rozvrh/privacy_policy.html")

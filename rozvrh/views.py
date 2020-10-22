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
    ("nej4", "nej4"),
    ("frj1", "frj1"),
    ("frj2", "frj2"),
    ("frj3", "frj3"),
    ("ruj", "ruj"),
    ("ruj1", "ruj1"),
    ("ruj2", "ruj2"),
]
SemS1 = [
    (" ", "Žádný"),
    ("zes1", "zes1"),
    ("chs1", "chs1"),
    ("fys1", "fys1"),
    ("sps1", "sps1"),
    ("bi1A", "bi1A"),
    ("bi1B", "bi1B"),
    ("des1", "des1"),
    ("eps1", "eps1"),
    ("kan1", "kan1"),
]
SemS2 = [
    (" ", "Žádný"),
    ("svs2", "svs2"),
    ("fys2", "fys2"),
    ("mas2", "mas2"),
    ("sps2", "sps2"),
    ("eps2", "eps2"),
    ("bis2", "bis2"),
    ("aw2", "aw2"),
]
SemS3 = [
    (" ", "Žádný"),
    ("chs3", "chs3"),
    ("ps2", "ps2"),
    ("mas3", "mas3"),
    ("sps3", "sps3"),
    ("eps3", "eps3"),
    ("kaz3", "kaz3"),
    ("dgs5", "dgs5"),
    ("ps3", "ps3"),
]
SemO4 = [
    (" ", "Žádná"),
    ("fsm4", "fsm4"),
    ("biv4", "biv4"),
    ("pss4", "pss4"),
    ("mvs4", "mvs4"),
    ("fis4", "fis4"),
    ("kaz4", "kaz4"),
]
SemO3 = [
    (" ", "Žádný"),
    ("psA3", "psA3"),
    ("biv3", "biv3"),
    ("psB3", "psB3"),
    ("anA3", "anA3"),
    ("msB3", "msB3"),
    ("dgs5", "dgs5"),
    ("anB3", "anB3"),
]
SemO1 = [
    (" ", "Žádná"),
    ("svs1", "svs1"),
    ("eps1", "eps1"),
    ("bis1", "bis1"),
    ("des1", "des1"),
    ("lis1", "lis1"),
    ("mas1", "mas1"),
]
SemO2 = [
    (" ", "Žádná"),
    ("chs2", "chs2"),
    ("svs2", "svs2"),
    ("bis2", "bis2"),
    ("fys2", "fys2"),
    ("zes2", "zes2"),
    ("pro2", "pro2"),
    ("lis2", "lis2"),
    ("eps2", "eps2"),
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
volitelne1 = [
    (" ", "Žádná"),
    ("mic", "mic"),
    ("vls", "vls"),
    ("skc", "skc"),
    ("ppc", "ppc"),
    ("gep", "gep"),
]
volitelne2 = [
    (" ", "Žádná"),
    ("mic", "mic"),
    ("vls", "vls"),
    ("skc", "skc"),
    ("ppc", "ppc"),
    ("gep", "gep"),
]
volitelne3 = [
    (" ", "Žádná"),
    ("dbkn", "dbkn"),
    ("desn", "desn"),
]

# Create your views here.
class RozvrhForm(forms.Form):
    trida = forms.ChoiceField(choices=classes, label="Třída")
    aj = forms.ChoiceField(choices=aj, label="Jazyková skupina")
    jazyk2 = forms.ChoiceField(choices=jazyk, label="Cizí jazyková skupina")
    volitelne1 = forms.ChoiceField(choices=volitelne1, label="Volitelné předměty 1")
    volitelne2 = forms.ChoiceField(choices=volitelne2, label="Volitelné předměty 2")
    volitelne3 = forms.ChoiceField(choices=volitelne3, label="Volitelné předměty 3")
    SemS1 = forms.ChoiceField(choices=SemS1, label="První seminář")
    SemS2 = forms.ChoiceField(choices=SemS2, label="Druhý seminář")
    SemS3 = forms.ChoiceField(choices=SemS3, label="Třetí seminář")
    SemO1 = forms.ChoiceField(choices=SemO1, label="První seminář")
    SemO2 = forms.ChoiceField(choices=SemO2, label="Druhý seminář")
    SemO3 = forms.ChoiceField(choices=SemO3, label="Třetí seminář")
    SemO4 = forms.ChoiceField(choices=SemO4, label="Čtvrtý seminář")
    skupina = forms.ChoiceField(choices=skupina, label="Skupina")
    gender = forms.ChoiceField(choices=gender, label="Pohlaví")


def index(request):
    if request.method == 'POST':
        form = RozvrhForm(request.POST)
        if form.is_valid():
            trida = form.cleaned_data['trida']
            aj = form.cleaned_data['aj']
            jazyk2 = form.cleaned_data['jazyk2']
            SemS1 = form.cleaned_data['SemS1']
            SemS2 = form.cleaned_data['SemS2']
            SemS3 = form.cleaned_data['SemS3']
            SemO1 = form.cleaned_data['SemO1']
            SemO2 = form.cleaned_data['SemO2']
            SemO3 = form.cleaned_data['SemO3']
            SemO4 = form.cleaned_data['SemO4']
            volitelne1 = form.cleaned_data['volitelne1']
            volitelne2 = form.cleaned_data['volitelne2']
            volitelne3 = form.cleaned_data['volitelne3']
            skupina = form.cleaned_data['skupina']
            gender = form.cleaned_data["gender"]
            PList = [aj, jazyk2, SemS1, SemS2, SemS3, SemO1, SemO2, SemO3, SemO4, volitelne1, volitelne2, volitelne3, skupina, gender, '']
            request.session['trida'] = trida
            request.session['PList'] = PList
        print(request.session['PList'])
        #if 'creds' not in request.session:
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        redirect_uri = 'https://bakalaricz.herokuapp.com/rozvrh/form'
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', SCOPES, redirect_uri=redirect_uri)
        flow.redirect_uri = "https://bakalaricz.herokuapp.com/rozvrh/form"
        authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes="true")
        request.session['state'] = state
        return HttpResponseRedirect(authorization_url)

    
    return render(request, "rozvrh/index.html", {
        "form": RozvrhForm(), 
        'worked': ""
    })
    
def rozvrhAdd(request):
    PList = request.session['PList']
    trida = request.session['trida']
    state = request.session['state']
    authorization_response = request.build_absolute_uri()
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    redirect_uri = 'https://bakalaricz.herokuapp.com/rozvrh/form'
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json', SCOPES, state=state, redirect_uri=redirect_uri)
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
    getTimeTable(trida, PList, request.session['creds'])
    return render(request, "rozvrh/rozvrh.html")

def greet(request, name):
    return render(request, "rozvrh/greet.html", {
        'name': name.capitalize()
    })                               

def PrivacyPolicy(request):
    return render(request, "rozvrh/privacy_policy.html")

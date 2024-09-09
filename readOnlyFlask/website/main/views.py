from re import I
from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from datetime import datetime
from langdetect import detect
import json
import requests
from . import main
from .forms import HindiInputForm
from .. import db
from ..models import User, PastInput, SavedTranslation
from flask_login import login_required, login_user, logout_user, current_user
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
shabdkhosh_bearer=os.getenv('shabdkhosh_bearer')
chatgpt_api_key=os.getenv('chatgpt_api_key')

@main.route('/', methods=['GET','POST'])
def readOnly():
    renderedHindiInputForm=HindiInputForm()
    if renderedHindiInputForm.validate_on_submit():  
        hindiInput1=renderedHindiInputForm.pastInput.data
        formSubmission=PastInput(pastInput=renderedHindiInputForm.pastInput.data,user=current_user._get_current_object())
        lang=detect(hindiInput1)
        if lang!='hi':
            flash("This Program Only Works for Hindi Text")
            return redirect(url_for('main.readOnly'))
        else:
            db.session.add(formSubmission)
            db.session.commit()
            flash("Let's Read Some Hindi!")
            form_submission_id=formSubmission.id
            return redirect(url_for('main.readOnlyMode', dataId=form_submission_id))
    pastInputs=PastInput.query.filter_by(user_id=current_user.id).order_by(PastInput.dateCreated.desc()).all()
    return render_template('readOnly.html', current_time=datetime.now(), renderedHindiInputForm=renderedHindiInputForm, pastInputs=pastInputs)

@main.route('/savedTranslations', methods=['GET','POST'])
def savedTranslations():
    pastInputs=PastInput.query.filter_by(user_id=current_user.id).all()
    savedTranslations=[]
    for pastInput in pastInputs:
        savedTranslations.extend(pastInput.savedTranslations)
    print('an array with savedTranslations', savedTranslations)
    return render_template('savedTranslations.html', savedTranslations=savedTranslations)

@main.route('/readOnlyMode/saveWordsEndpoint', methods=['GET', 'POST'])
def save_word():
    wordJSON=json.loads(json.dumps(request.get_json(), ensure_ascii=False))
    englishTranslations=""
    n=1000
    for key, value in wordJSON.items():
        if key=='hindi':
            hindiWord=value
            continue
        englishTranslations=englishTranslations+key+': '+value+'\n'
    myTranslations=SavedTranslation(id=n+1, hindiWord=hindiWord, englishTranslations=englishTranslations)
    db.session.add(myTranslations)
    db.session.commit()

    return "We saved words"

@main.route('/readOnlyMode/translationEndpoint', methods=['GET', 'POST'])
def get_translation_info():
    url="https://www.shabdkosh.com/dictapi"
    cookies = {'exp_last_activity': '1725894095', 
                    'exp_last_visit':'1725459360'
                    }
    headers={'Custom-Header':'ZdkpnE9',
                    'Content-Encoding':'br',
                    'User-Agent':'readOnly',
                    'Cache-Control':'no-cache',
                    "Content-Type": "application/json; charset=utf-8",
                    'Authorization': shabdkhosh_bearer}
    user_selection_dict=json.loads(json.dumps(request.get_json(), ensure_ascii=False)) 
    type=user_selection_dict['type']
        
    if(type=='word'):
        foreign_word=user_selection_dict['selection']
        params= {
                'e':foreign_word,
                't':'1',
                'l':'hi',
                'v':'3',
                }
        r=requests.post(url=url,cookies=cookies,headers=headers, params=params)
        print(r.url)
        
            #formatted JSON object, meant for debugging
        json_object=json.dumps(r.json(),  ensure_ascii=False, indent=2)
        print(json_object)

        shabd_json = json.loads(json_object) #json object returned by shabdkhosh  
            
        ##romanized_word=shabd_json["p"][0]["ps"][0]
        translation_info_json=shabd_json["t"]
    return translation_info_json

#In progress endpoint for phrase translations
@main.route('/readOnlyMode/chatGPTEndpoint', methods=['GET', 'POST'])
def get_phrase_translation_info():
    user_selection_dict=json.loads(json.dumps(request.get_json(), ensure_ascii=False)) 
    foreign_text=user_selection_dict['selection']
    attempted_translation=user_selection_dict['attemptedTranslation']
    client = OpenAI(api_key=chatgpt_api_key)
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
                {   "role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",
                    "content": f'Are there any errors in this Hindi translation? Hindi: {foreign_text} English: {attempted_translation}'
                }
            ]
    )
    phrase_translation_json=completion.choices[0].message
    return phrase_translation_json

@main.route('/readOnlyMode/<int:dataId>', methods=['GET', 'POST'])
@login_required
def readOnlyMode(dataId):
    user_url = url_for('main.readOnlyMode', dataId=dataId) 
    if not dataId:
        return redirect(url_for('main.noReadOnlyMode'))
    dataObject=PastInput.query.get(dataId)
    if not dataObject:
        return "Data not found", 404
    renderedText=dataObject.pastInput
    return render_template('readOnlyMode.html', dataId=dataId, user_url=user_url, renderedText=renderedText)


# to activate the app in cmd ".\\env\Scripts\activate"
# to run the app "flask run"

import datetime
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&appid=d5ed97edccf5d24a177d9c380f32403b'
    r = requests.get(url).json()
    return r
def get_weather_data_5(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={ city }&units=metric&appid=d5ed97edccf5d24a177d9c380f32403b'
    r1 = requests.get(url).json()
    return r1
@app.route('/')
def index_get():
   

    cities = City.query.all()
     
    weather_data = []

    for city in cities:

        r = get_weather_data(city.name)  

        print(r)

        r1 = get_weather_data_5(city.name)
        print("##############")
        print(r1)

        weather = {
            'city' : city.name,
            'temperature' : round(r['main']['temp']),
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)

@app.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()
        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'Orasul nu exista!'
        else:
            err_msg = 'Orasul este deja afisat!'
    
    if err_msg:
        flash(err_msg, 'error')
    else:
        flash('Oras afisat cu succes!')
    return redirect(url_for('index_get'))

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Orasul { city.name } sters cu succes!', 'success')

    return redirect(url_for('index_get'))

@app.route('/chartjs/')
def chartjs():
    
    # new_city = request.form.get('city')

    # if new_city:
    #     existing_city = City.query.filter_by(name=new_city).first()
    #     if not existing_city:
    #         new_city_data = get_weather_data_5(new_city)
    #         if new_city_data['cod'] == 200:
    #             new_city_obj = City(name=new_city)
    #             db.session.add(new_city_obj)
    #             db.session.commit()

    # cities = City.query.all()

    # for city in cities:

    r1 = get_weather_data_5('Las Vegas') 
    
    reportTime1 = datetime.datetime.utcfromtimestamp(r1['list'][0]['dt']).strftime('%d %b %Y')
    report2 = datetime.datetime.utcfromtimestamp(r1['list'][4]['dt']).strftime('%d %b %Y')
    reportt3 = datetime.datetime.utcfromtimestamp(r1['list'][12]['dt']).strftime('%d %b %Y')
    reporttt4 = datetime.datetime.utcfromtimestamp(r1['list'][20]['dt']).strftime('%d %b %Y')
    reporty5 = datetime.datetime.utcfromtimestamp(r1['list'][28]['dt']).strftime('%d %b %Y')

    weather_days=[reportTime1, report2, reportt3,
     reporttt4, reporty5]
    
    weather_temp=[round(r1['list'][0]['main']['temp']), round(r1['list'][4]['main']['temp']),
     round(r1['list'][12]['main']['temp']), round(r1['list'][20]['main']['temp']), round(r1['list'][28]['main']['temp'])]
    
    return render_template('chartjs.html', labels=weather_days, values=weather_temp)
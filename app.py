from flask import Flask, render_template, url_for, redirect, request, jsonify, Response
import pyrebase
import json
import pickle
import pandas as pd
from settings import *
from UserModel import User

import jwt, datetime

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyDoanF74Vz7-7la5QwtsnXJeaWD1P9yxX0",
    "authDomain": "fraud-detection-e8f47.firebaseapp.com",
    "databaseURL": "https://fraud-detection-e8f47.firebaseio.com",
    "projectId": "fraud-detection-e8f47",
    "storageBucket": "",
    "messagingSenderId": "769528097628",
    "appId": "1:769528097628:web:88365ba191529a635b2f99"
}

app.config['SECRET_KEY'] = 'hola'

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route('/', methods = ['GET', 'POST'])
def index():

    unsuccessful = 'Please check your credentials'
    successful = 'Login Successful'

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('logout.html', s = successful)
        except:
            return render_template('login.html', us = unsuccessful)

    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    register_successful = 'Sign in now!'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return redirect(url_for('index'), register_successful = register_successful)
    return render_template('register.html', register_successful = register_successful)

#Load Logistic regression model
loaded_model = pickle.load(open('logistic_model.sav', 'rb'))

@app.route('/verify', methods = ['POST'])
def predict():
    token = request.args.get ('token')

    try:
        jwt.decode(token, app.config['SECRET_KEY'])
        transaction = pd.DataFrame(request.get_json(),index = [0])
        print(transaction)
        prediction = str(loaded_model.predict(transaction))
        result ={'prediction':prediction}
    except:
        return jsonify({'error':'Need a valid token to view this page'})
    return jsonify(result)

@app.route('/login',methods = ['POST'])
def get_token():
    request_data = request.get_json()
    username = str (request_data['username'])
    password = str (request_data['password'])

    match = User.username_password_match(username,password)
    #If the username and password match with database
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds =100)
        token = jwt.encode({'exp': expiration_date},app.config['SECRET_KEY'],algorithm ='HS256')
        return token
    else:
        return Response ('',401,mimetype ='application/json')


if __name__ == "__main__":
    app.run(debug = True)
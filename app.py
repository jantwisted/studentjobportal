from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import requests
import json
import jwt

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCN5UwzussKx2SSNjo-qJla0f3aGr-KnmQ"
app.secret_key = os.urandom(12)
GoogleMaps(app)

api_url = 'http://127.0.0.1:8080'

jwt_token = ''

def get_all_jobs(latitude, longitude):
    print(latitude)
    print(longitude)
    url = api_url+'/jobs/all'
    print(url)
    headers = {'Authorization': 'Bearer '+jwt_token}
    response = requests.get(url, headers=headers)
    jobs_list = json.loads(response.text)
    return jobs_list


def build_marker(jobs_list):
    markers = []
    for job in jobs_list:
        job_shw = {
	'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
	'lat':  float(job['Latitude']),
	'lng':  float(job['Longtitude']),
	'infobox': job['Short_desc']
	}
        markers.append(job_shw)

    return markers



@app.route('/')
def home(latitude='', longitude=''):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        jobs_list = get_all_jobs(latitude, longitude)
        markers = build_marker(jobs_list)
        sndmap = Map(
            identifier="sndmap",
            style="height:600px;width:100%;margin:0;",
            zoom=15,
            lat=47.087734,
            lng=17.922842,
            markers=[
            ]
        )
        sndmap.markers = markers
        return render_template('home.html', sndmap=sndmap)


@app.route('/login', methods=['POST'])
def do_admin_login():
    user_details = {}
    print(request.form)
    user_name = request.form['username']
    user_password = request.form['password']
    current_latitude = request.form['latitude']
    current_longitude = request.form['longitude']
    user_details['UserName'] = user_name
    user_details['Password'] = user_password
    url = api_url+'/users/login'
    body = user_details
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    response_dict = json.loads(response.text)
    global jwt_token
    jwt_token = response_dict['JWT']
    try:
        claim = jwt.decode(response_dict['JWT'], algorithms=['HS256'], verify=False)
        if claim['user'] == user_name:
            session['logged_in'] = True
        else:
            flash('wrong password!')
    except jwt.DecodeError:
        flash('wrong credentials!')
    return home(current_latitude, current_longitude)

@app.route("/showregister")
def showregister():
    return render_template('register.html')

@app.route("/register", methods=['POST'])
def register():
    user_details = {}
    print(request.form)
    user_name = request.form['userName']
    user_password = request.form['inputPassword']
    user_firstname = request.form['firstName']
    user_lastname = request.form['lastName']
    user_email = request.form['inputEmail']
    user_type = "student"
    user_status = "1"
    user_details['UserName'] = user_name
    user_details['Password'] = user_password
    user_details['FirstName'] = user_firstname
    user_details['LastName'] = user_lastname
    user_details['UserType'] = user_type
    user_details['UserStatus'] = user_status
    user_details['Email'] = user_email
    url = api_url+'/users/add'
    body = user_details
    print(body)
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    response_dict = json.loads(response.text)
    if response_dict['Action'] == 'register':
        if response_dict['Result'] == 'true':
            flash('successfully registered')
        else:
            flash('something went wrong')
    else:
        flash('wrong msg type')
    return home()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



if __name__ == "__main__":
    app.run()

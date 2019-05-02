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
GoogleMaps(app)

api_url = 'https://studentjobengine.herokuapp.com'

jwt_token = ''

def get_all_jobs():
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
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        jobs_list = get_all_jobs()
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
    user_name = request.form['username']
    user_password = request.form['password']
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
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()

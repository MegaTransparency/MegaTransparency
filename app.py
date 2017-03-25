import urllib
import os
import uuid
import requests
import stripe
import json
import flask
from flask import Flask, render_template, request, redirect, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_failsafe import failsafe
import calendar
import time
app = Flask(__name__)
socketio = SocketIO(app)
from threading import Thread
thread = None
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.expression import cast

app.config.from_pyfile('_config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import re
import models
from sqlalchemy.sql import text


from flask_oauth import OAuth

oauth = OAuth()
from flask_cors import CORS, cross_origin

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

stripe_keys = {
  'secret_key': app.config['STRIPE_SECRET_KEY'],
  'publishable_key': app.config['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

REDIRECT_URI = 'https://devapi.wayeasycorp.com/api/oauth/google'

def get_user(request):
    session_uid = session.get('session_uid') if session.get('session_uid') else request.args.get('session_uid')
    print session_uid
    if not session_uid:
        return None
    q = db.session.query(models.Session).filter(models.Session.uid == session_uid)
    if q.first():
        if q.first().active:
            return db.session.query(models.User).filter(models.User.user_id == q.first().user_id).first()
        else:
            return None
    else:
        return None 

@app.route('/api/is_logged_in', strict_slashes=False)
def is_logged_in():
    return flask.jsonify(is_logged_in=bool(get_user(request)))
    
@app.route('/api/set_session', strict_slashes=False)
def set_session():
    if session.get('oauth_id'):
        session['oauth_id'] = session['oauth_id'].strip()
    access_token = session.get('access_token')
    session_uid = session.get('session_uid')
    if access_token is None:
        return redirect(url_for('login'))
 
    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError
 
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
    oauth_data = json.loads(res.read())
    session['oauth_id'] = oauth_data['id']
    
    if not db.session.query(models.Oauth).filter(models.Oauth.oauth_id == session.get('oauth_id')).count():
        #Create the db user
        user_data = oauth_data
        user_data['created_at'] = calendar.timegm(time.gmtime())*1000
        new_user = models.User(
            data = user_data
        )
        db.session.add(new_user)
        db.session.commit()
        new_oauth = models.Oauth(
            user_id = new_user.user_id,
            provider = 'google',
            access_token = access_token,
            oauth_id = oauth_data['id'],
            data = oauth_data
        )
        db.session.add(new_oauth)
        db.session.commit()
    oauth_in_db = db.session.query(models.Oauth).filter(models.Oauth.oauth_id == session.get('oauth_id')).first()
    oauth_in_db.data = oauth_data
    oauth_in_db.access_token = access_token
    db.session.commit()
    user_in_db = db.session.query(models.User).filter(models.User.user_id == oauth_in_db.user_id).first()
    if  user_in_db.data:
        d = oauth_data
        user_in_db.data.update(d)
    else:
        d = oauth_data
        user_in_db.data = d
    db.session.commit()
    user_id = db.session.query(models.Oauth).filter(models.Oauth.oauth_id == session.get('oauth_id')).first().user_id
    q = db.session.query(models.Session).filter(models.Session.uid == session.get('session_uid'))
    if session_uid is None:
        session_uid = str(uuid.uuid4())
        new_session = models.Session(
            uid = session_uid,
            user_id = user_id,
            active = True
        )
        db.session.add(new_session)
        db.session.commit()
        session['session_uid'] = new_session.uid
        session_in_db = q.first()
    else:
        session_in_db = q.first()
        if session_in_db:
            if session_in_db.active == False:
                for key in session.keys():
                    session.pop(key, None)
                redirect(url_for('login'))
        else:
            for key in session.keys():
                session.pop(key, None)
                redirect(url_for('login'))
    session['oauth_id'] = oauth_data['id']
    next = request.args.get('next', '/')
    if next.startswith('https://'):
        import urllib
        next = next + '?' + urllib.urlencode({'access_token': access_token, 'session_uid': session_uid})
    return redirect(next)
 

google = oauth.remote_app('google',
          base_url='https://www.google.com/accounts/',
          authorize_url='https://accounts.google.com/o/oauth2/auth',
          request_token_url=None,
          request_token_params={'prompt': 'select_account', 'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/user.birthday.read',
                                'response_type': 'code', 'state': ''},
          access_token_url='https://accounts.google.com/o/oauth2/token',
          access_token_method='POST',
          access_token_params={'grant_type': 'authorization_code'},
          consumer_key=app.config['GOOGLE_CLIENT_ID'],
          consumer_secret=app.config['GOOGLE_CLIENT_SECRET'])

@app.route('/login', strict_slashes=False)
def login():
    next=request.args.get('next') or request.referrer or ''
    callback=url_for('authorized', _external=True, _scheme='https')
    google.request_token_params.update({'state': next})
    return google.authorize(callback=callback)
 
 
 
@app.route('/api/oauth/google')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    next=request.args.get('state', '')
    print 'next', next
    print 'next', next, url_for('set_session', next=next)
    
    return redirect(url_for('set_session', next=next))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')

@app.route('/logout')
def logout():
    try:
        q = db.session.query(models.Session).filter(models.Session.uid == session.get('session_uid'))
        session_in_db = q.first()
        session_in_db.active = False
        db.session.commit()
    except AttributeError:
        pass
    for key in session.keys():
        session.pop(key, None)
    
    return redirect('/')


@app.errorhandler(404) # We always return index.html if route not found because we use Vue.JS routing
def page_not_found(e):
    return app.send_static_file('index.html'), 200

@app.route('/api/server_time', strict_slashes=False)
def server_time():
    return flask.jsonify(datetime=calendar.timegm(time.gmtime())*1000)


@app.route('/charge', methods=['POST'], strict_slashes=False)
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)    

    
@failsafe
def create_app():
    return app

import eventlet
eventlet.monkey_patch()
if __name__ == '__main__':
    socketio.run(create_app(), debug=True, port=app.config['PORT'])
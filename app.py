import urllib
import os
import uuid
import requests
import stripe
import json
import flask
from flask import Flask, render_template, request, redirect, session, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_failsafe import failsafe
import calendar
import time
import jinja2
app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
socketio = SocketIO(app)
from threading import Thread
thread = None
from sqlalchemy.dialects.postgresql import JSONB, JSON
from sqlalchemy.sql.expression import cast, func
import psycopg2
import psycopg2.extras
import traceback
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

REDIRECT_URI = 'https://devapi.wayeasycorp.com/oauth/google'

def get_user(request):
    session_uuid = session.get('session_uuid') if session.get('session_uuid') else request.args.get('session_uuid')
    print session_uuid
    if not session_uuid:
        return None
    q = db.session.query(models.Session).filter(models.Session.secret_uuid == session_uuid)
    if q.first():
        if q.first().active:
            return db.session.query(models.User).filter(models.User.user_uuid == q.first().user_uuid).first()
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
    session_uuid = session.get('session_uuid')
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
            user_uuid = new_user.user_uuid,
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
    user_in_db = db.session.query(models.User).filter(models.User.user_uuid == oauth_in_db.user_uuid).first()
    if  user_in_db.data:
        d = oauth_data
        user_in_db.data.update(d)
    else:
        d = oauth_data
        user_in_db.data = d
    db.session.commit()
    user_uuid = db.session.query(models.Oauth).filter(models.Oauth.oauth_id == session.get('oauth_id')).first().user_uuid
    q = db.session.query(models.Session).filter(models.Session.secret_uuid == session.get('session_uuid'))
    if session_uuid is None:
        new_session = models.Session(
            user_uuid = user_uuid,
            active = True
        )
        db.session.add(new_session)
        db.session.commit()
        session['session_uuid'] = new_session.secret_uuid
        session_in_db = q.first()
    else:
        session_in_db = q.first()
        session_in_db.user_uuid = user_uuid
        session_in_db.active = True
        db.session.commit()
        if session_in_db:
            if session_in_db.active == False:
                redirect(url_for('login'))
        else:
            redirect(url_for('login'))
    session['oauth_id'] = oauth_data['id']
    next = request.args.get('next', '/')
    if next.startswith('https://'):
        import urllib
        next = next + '?' + urllib.urlencode({'access_token': access_token, 'session_uuid': session_uuid})
    return redirect(next)
 

google = oauth.remote_app('google',
          base_url='https://www.google.com/accounts/',
          authorize_url='https://accounts.google.com/o/oauth2/auth',
          request_token_url=None,
          request_token_params={'prompt': 'select_account', 'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
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
 
 
 
@app.route('/oauth/google', strict_slashes=False)
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
        q = db.session.query(models.Session).filter(models.Session.secret_uuid == session.get('session_uuid'))
        session_in_db = q.first()
        session_in_db.active = False
        db.session.commit()
    except AttributeError:
        pass
    return redirect('/')

import signal
import time

class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

@app.route('/api/query_public_data')
def query_public_data():
    try:
        conn = psycopg2.connect("dbname='megatransparency' user='public_data_query' host='localhost' password='%s' options='-c statement_timeout=3s'" % (app.config['PUBLIC_DATA_QUERY_PASSWORD']))
    except:
        return flask.jsonify(success=False, error="can't connect to database as public query user")
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = request.args.get('sql', request.form.get('sql'))
        if not sql:
            return flask.jsonify(success=False, error='sql query is missing')
        cur.execute(sql)
        data_to_return = [dict([(col[0], str(col[1])) for col in dict(row).items()]) for row in cur.fetchall()]
        columns = [{'name': row[0], 'type': row[1]} for row in cur.description]
        return flask.jsonify(success=True, data=data_to_return, sql=sql, columns=columns)
        cur.close()
        conn.close()
    except Exception, e:
        error = traceback.format_exc()
        if 'canceling statement due to statement timeout' in error:
            error = "query didn't finish within the required three seconds"
        return flask.jsonify(success=False, error=error)

@app.before_request
def log_page_view():
    if not ('update_page_view' in request.path or 'set_session' in request.path or 'oauth' in request.path or 'ico' in request.path or 'static' in request.path):
        
        session_uuid = session.get('session_uuid')
        if session_uuid: # validate the session uuid
            if not db.session.query(models.Session).filter(models.Session.secret_uuid == session.get('session_uuid')):
                session_uuid = None
        if not session_uuid:
            new_session = models.Session(
                active = False
            )
            db.session.add(new_session)
            db.session.commit()
            session['session_uuid'] = new_session.secret_uuid
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ',' in ip_address:
            ip_address = ip_address.split(',')[0]
        data = {"ip_address": ip_address}
        session_data = db.session.query(models.Session).filter(models.Session.secret_uuid == session.get('session_uuid')).first()
        data['session_public_uuid'] = str(session_data.public_uuid)
        data['is_logged_in'] = session_data.active
        data['url'] = request.url
        if '?' in data['url']:
            data['url'] = data['url'][:request.url.index('?')]
        data['time_arrived'] = calendar.timegm(time.gmtime())*1000
        data['referrer'] = request.referrer
        if data['referrer']:
            if data.get('referrer', '').startswith('https://megatransparency.com/'):
                if '?' in data.get('referrer', ''):
                    data['referrer'] = data['referrer'][:request.url.index('?')]
            if data['referrer'].startswith('https://accounts.google.com/AccountChooser'):
                data['referrer'] = 'https://accounts.google.com/AccountChooser'
        data['post_data'] = dict(request.form)
        data['get_data'] = dict(request.args)
        if 'session_uuid' in data['get_data']:
            del data['get_data']['session_uuid']
        if 'session_uuid' in data['get_data']:
            del data['get_data']['access_token']
        print 'SESSION DATA', session_data.user_uuid
        if session_data.user_uuid:
            data['user_uuid'] = str(session_data.user_uuid)
            db.session.query(models.PageViews).filter(models.PageViews.data['session_public_uuid'].astext == str(session_data.public_uuid)).update({'data': cast(cast(models.PageViews.data, JSONB)
                           .concat(func.jsonb_build_object('user_uuid', str(session_data.user_uuid))), JSON)}, synchronize_session="fetch")
        user_agent = request.user_agent
        for key in ['platform', 'browser', 'version', 'language', 'string']:
            data['user_agent_'+key] = getattr(user_agent, key)
        new_page_view = models.PageViews(
            data = data
        )
        db.session.add(new_page_view)
        db.session.commit()
        print db.session.query(models.PageViews).filter(models.PageViews.uuid == new_page_view.uuid).first().data
        g.new_page_view_uuid = new_page_view.uuid

def look_up_page_title_and_description(request):
    page_title = ''
    page_description = ''
    print "request path", request.path
    if request.path == '' OR request.path == '/':
        page_title = 'Home'
        page_description = "A site aiming to efficiently publish all the world's interesting public information in one well organized place"
    if request.path.startswith('public_activity_log'):
        page_title = 'Public Activity Log'
        page_description = 'All identifying info about non-subscribers.'
    return (page_title, page_description)

@app.errorhandler(404) # We always return index.html if route not found because we use Vue.JS routing
def page_not_found(e):
    page_title, page_description = look_up_page_title_and_description(request)
    return render_template('index.html', page_view_uuid=g.new_page_view_uuid, page_title=page_title)

@app.route('/api/update_page_view', strict_slashes=False, methods=['POST'])
def update_page_view():
    time_left = calendar.timegm(time.gmtime())*1000
    uuid = request.form['uuid']
    data = json.loads(request.form['data'])
    cleaned_data = {"time_left": time_left}
    for key in data:
        if key in ['mouse_locations', 'scrolls', 'screen_width', 'screen_height']:
            cleaned_data[key] = data[key]
    page_view_in_db = db.session.query(models.PageViews).filter(models.PageViews.uuid == uuid).first()
    print 'page view in db', page_view_in_db
    if page_view_in_db:
        # for whatever reason modifying page_view_in_db.data then doing db.session.commit() didn't update the page_view row
        page_view_in_db.data.update(cleaned_data)
        db.session.query(models.PageViews).filter(models.PageViews.uuid == uuid).update(dict(data=page_view_in_db.data))
        try:
            db.session.commit()
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            db.session.rollback()
            db.session.flush()
    return flask.jsonify(success=True)

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

import os
os.system('wget https://raw.githubusercontent.com/carltonnorthern/nickname-and-diminutive-names-lookup/master/names.csv -O nicknames.csv')
with open('nicknames.csv', 'r') as f:
    lines = f.readlines()
nicknames_to_groups = {}
i = 1
for line in lines:
    nicknames = [name.strip() for name in line.split(',') if name.strip()]
    group = None
    for nickname in nicknames:
        if nickname in nicknames_to_groups:
            group = nicknames_to_groups[nickname]
            break
    if group:
        for nickname in nicknames:
            nicknames_to_groups[nickname] = group
    else:
        for nickname in nicknames:
            nicknames_to_groups[nickname] = i
        i += 1

import flask
from flask import Flask, render_template, request, redirect, session, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_failsafe import failsafe
app = Flask(__name__)
app.config.from_pyfile('../_config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import sys
sys.path.append('../')
import models

for row in nicknames_to_groups.items():
    new_name = models.Nicknames(
        name = row[0],
        groupi = row[1]
    )
    db.session.add(new_name)
    db.session.commit()

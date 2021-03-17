import datetime

# create database
from app import db
db.create_all()

# Add user to the database
from app.models import User, generate_password_hash
usr = input ('username: ')
pwd = input ('password: ')
new_user = User(username=usr, password_hash=generate_password_hash(pwd))
db.session.add(new_user)

# Add default site info
from app.models import Site

description = Site(name='desc', value='A simple blog')
title = Site(name='title', value='Hello World!')
home_html = Site(name='home_html', value='This is a self-hosted weblog')

draft_description = Site(name='draft_desc', value='A simple blog')
draft_title = Site(name='draft_title', value='Hello World!')
draft_home_html = Site(name='draft_home_html', value='This is a self-hosted weblog')

last_updated = Site(name='updated_date', value=datetime.date.today())

db.session.add(description)
db.session.add(title)
db.session.add(home_html)

db.session.add(draft_description)
db.session.add(draft_title)
db.session.add(draft_home_html)

db.session.add(last_updated)

# commit changes to database
db.session.commit()

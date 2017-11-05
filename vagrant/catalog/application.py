#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, Flask, render_template, redirect, jsonify, url_for
from flask import make_response, session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db.db_setup import Base, User, Catalog, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from unicodedata import normalize
import httplib2
import requests
import json
import string
import random

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
session = sessionmaker(bind=engine)()


@app.route('/')
def index():
    catalogs = session.query(Catalog).all()
    items = session.query(Item).all()
    result = {}

    for catalog in catalogs:
        for item in items:
            if item.catalog_name == catalog.name:
                catalog_name = normalize('NFKD', catalog.name).encode('ascii','ignore')
                item_name = normalize('NFKD', item.name).encode('ascii','ignore')
                item_description = normalize('NFKD', item.description).encode('ascii','ignore')
                if not result.get(catalog_name):
                    result[catalog_name] = {}
                result[catalog_name][item_name] = item_description

    return render_template('index.html', result = result)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/add', methods=['GET', 'POST'])
def addCatalogItem():
    return render_template('add.html')


@app.route('/catalog/<catalog>/<item>')
def catalogItem(catalog, item):
    result = session.query(Item).filter_by(name=item).one_or_none()
    return render_template(
        'detail.html',
        catalog=catalog,
        item=item,
        description=result.description,
        isLogin=False
    )


@app.route('/catalog/<catalog>/<item>/edit', methods=['GET', 'POST'])
def editCatalogItem(catalog, item):
    return 'EDIT: catalog: ' + catalog + ' item: ' + item


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

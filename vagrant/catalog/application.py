#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, jsonify, url_for
from flask import make_response, session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db.db_setup import Base, User, Catalog, Item 
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json
import string
import random

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
session = sessionmaker(bind=engine)


@app.route('/')
def index():
	return 'home'


@app.route('/catalog/<catalog>/items')
def catalogItems(catalog):
	return 'catalog items: ' + catalog


@app.route('/new', methods=['GET', 'POST'])
def addCatalogItem():
	return 'new catalog item'


@app.route('/catalog/<catalog>/<item>', methods=['GET', 'POST'])
def catalogItem(catalog, item):
	return 'catalog: ' + catalog + ' item: ' + item


@app.route('/catalog/<catalog>/<item>/edit', methods=['GET', 'POST'])
def editCatalogItem(catalog, item):
	return 'EDIT: catalog: ' + catalog + ' item: ' + item


@app.route('/catalog/<catalog>/<item>/delete', methods=['GET', 'POST'])
def deleteCatalogItem(catalog, item):
	return 'DELETE: catalog: ' + catalog + ' item: ' + item


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

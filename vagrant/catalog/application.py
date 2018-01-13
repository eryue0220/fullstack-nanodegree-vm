#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, Flask, render_template, redirect, jsonify, url_for
from flask import make_response, session as login_session, flash
from sqlalchemy import asc
from db.db_setup import Catalog, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from unicodedata import normalize
from db_session import db_session
from user import get_user_id, create_user
import httplib2
import requests
import json
import string
import random

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('google_client_secret.json', 'r').read())['web']['client_id']


@app.route('/')
def index():
    catalogs = db_session.query(Catalog).all()
    items = db_session.query(Item).all()
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

    return render_template(
        'index.html',
        result = result,
        is_login = login_session.get('user_name')
    )


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    if request.method == 'GET' and 'user_name' not in login_session:
        return render_template('signin.html', STATE=state)
    elif 'user_name' in login_session:
        return redirect(url_for('index'))


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    del login_session['user_name']
    del login_session['email']
    del login_session['user_id']
    return redirect(url_for('index'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if requests.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = requests.data
    try:
        oauth_flow = flow_from_clientsecrets('google_client_secret.json',
            scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorized code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
        % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            joson.dumps('Token user id doesn\'t match given id'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        reposne = make_response(json.dumps('Current User signin'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {
        'access_token': credentials.access_token
    }


@app.route('/gdisconnect', methods=['POST'])
def gdisconnect():
    pass


@app.route('/add/catalog', methods=['GET', 'POST'])
def addCatalog():
    if request.method == 'GET': 
        return render_template('add.html')

    if request.method == 'POST':
        form = request.form
        catalogName = form['catalog'].lower()
        query = db_session.query(Catalog).filter_by(name=catalogName).one_or_none()

        if not query:
            catalog = Catalog(name=catalogName)
            db_session.add(catalog)
            db_session.commit()
            return redirect(url_for('index'))
        else:
            flash('Current Catalog has existed.')
            return render_template('add.html')


@app.route('/add/item', methods=['GET', 'POST'])
def addItem():
    catalogs = db_session.query(Catalog).all()
    if request.method == 'GET':
        return render_template('add_item.html', catalogs=catalogs)

    if request.method == 'POST':
        form = request.form
        name = form['name']
        catalogName = form['catalog']
        description = form['description']
        query = db_session.query(Item).filter_by(name=name).one_or_none()

        if not query:
            new_item = Item(
                name=name,
                catalog_name=catalogName,
                description=description
            )
            db_session.add(new_item)
            db_session.commit()
            return redirect(url_for('index'))
        else:
            flash('Item Name has existed.')
            return render_template('add_item.html', catalogs=catalogs)


@app.route('/catalog/<catalog>/<item>')
def catalogItem(catalog, item):
    result = db_session.query(Item).filter_by(name=item).one_or_none()
    return render_template(
        'detail.html',
        catalog=catalog,
        item=item,
        description=result.description,
        is_login=True
    )


@app.route('/catalog/<catalog>/<item>/edit', methods=['GET', 'POST'])
def editCatalogItem(catalog, item):
    selected_item = db_session.query(Item).filter_by(name=item).one_or_none()
    hasChange = False

    if request.method == 'GET':
        all_catalogs = db_session.query(Catalog).all()
        return render_template(
            'edit.html',
            catalog=catalog,
            all_catalogs=all_catalogs,
            item=selected_item
        )

    # Update Item
    if request.method == 'POST':
        form = request.form
        if form['name'] and form['name'] != selected_item.name:
            selected_item.name = form['name']
            hasChange = True

        if form['description'] and form['description'] != selected_item.description:
            selected_item.description = form['description']
            hasChange = True

        if form['catalog'] and form['catalog'] != selected_item.catalog.name:
            selected_item.catalog_name = form['catalog']
            hasChange = True

        if hasChange:
            db_session.add(selected_item)
            db_session.commit()

        return redirect(url_for(
            'catalogItem',
            catalog=selected_item.catalog_name,
            item=selected_item.name
        ))


# delete operation api
@app.route('/api/v1/catalog/<item>/delete')
def deleteItem(item):
    selected_item = db_session.query(Item).filter_by(name=item).one_or_none()
    db_session.delete(selected_item)
    db_session.commit()
    response = {'status': 0, 'msg': 'Delete Success'}
    return jsonify(response), 200


# JSON APIs
@app.route('/api/v1/catalogs.json')
def catalogs_api():
    result = db_session.query(Catalog).all()
    return jsonify([i.serialize for i in result])


@app.route('/api/v1/catalog/<catalog>.json')
def catalog_api(catalog):
    query = db_session.query(Item).filter_by(catalog_name=catalog).all()
    result = []
    for i in query:
        result.append({
            'name': i.name,
            'description': i.description,
            'catalog': i.catalog.name
        })
    return jsonify(result)


@app.route('/api/v1/catalog/<item>.json')
def catalog_item_api(item):
    result = db_session.query(Item).filter_by(name=item).one_or_none()
    CatalogItem = {
        'name': result.name,
        'description': result.description,
        'catalog': result.catalog.name
    }
    return jsonify(CatalogItem=CatalogItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

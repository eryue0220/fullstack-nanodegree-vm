#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import request, Flask, render_template, redirect, jsonify, url_for
from flask import make_response, session as login_session, flash
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


@app.route('/add/catalog', methods=['GET', 'POST'])
def addCatalog():
    if request.method == 'GET': 
        return render_template('add.html')

    if request.method == 'POST':
        form = request.form
        catalogName = form['catalog'].lower()
        query = session.query(Catalog).filter_by(name=catalogName).one_or_none()

        if not query:
            catalog = Catalog(name=catalogName)
            session.add(catalog)
            session.commit()
            return redirect(url_for('index'))
        else:
            flash('Current Catalog has existed.')
            return render_template('add.html')


@app.route('/add/item', methods=['GET', 'POST'])
def addItem():
    catalogs = session.query(Catalog).all()
    if request.method == 'GET':
        return render_template('add_item.html', catalogs=catalogs)

    if request.method == 'POST':
        form = request.form
        name = form['name']
        catalogName = form['catalog']
        description = form['description']
        query = session.query(Item).filter_by(name=name).one_or_none()

        if not query:
            new_item = Item(
                name=name,
                catalog_name=catalogName,
                description=description
            )
            session.add(new_item)
            session.commit()
            return redirect(url_for('index'))
        else:
            flash('Item Name has existed.')
            return render_template('add_item.html', catalogs=catalogs)


@app.route('/catalog/<catalog>/<item>')
def catalogItem(catalog, item):
    result = session.query(Item).filter_by(name=item).one_or_none()
    return render_template(
        'detail.html',
        catalog=catalog,
        item=item,
        description=result.description,
        is_login=True
    )


@app.route('/catalog/<catalog>/<item>/edit', methods=['GET', 'POST'])
def editCatalogItem(catalog, item):
    selected_item = session.query(Item).filter_by(name=item).one_or_none()
    hasChange = False

    if request.method == 'GET':
        all_catalogs = session.query(Catalog).all()
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
            session.add(selected_item)
            session.commit()

        return redirect(url_for(
            'catalogItem',
            catalog=selected_item.catalog_name,
            item=selected_item.name
        ))


# delete operation api
@app.route('/api/v1/catalog/<item>/delete')
def deleteItem(item):
    selected_item = session.query(Item).filter_by(name=item).one_or_none()
    session.delete(selected_item)
    session.commit()
    response = {'status': 0, 'msg': 'Delete Success'}
    return jsonify(response), 200


# JSON APIs
@app.route('/api/v1/catalogs.json')
def catalogs_api():
    result = session.query(Catalog).all()
    return jsonify([i.serialize for i in result])


@app.route('/api/v1/catalog/<catalog>.json')
def catalog_api(catalog):
    query = session.query(Item).filter_by(catalog_name=catalog).all()
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
    result = session.query(Item).filter_by(name=item).one_or_none()
    CatalogItem = {
        'name': result.name,
        'description': result.description,
        'catalog': result.catalog.name
    }
    return jsonify(CatalogItem=CatalogItem)


if __name__ == '__main__':
    app.secret_key = 'cin_chen'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

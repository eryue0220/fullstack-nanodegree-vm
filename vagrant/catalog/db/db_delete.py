#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Catalog, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.engine = engine
session = sessionmaker(bind=engine)()

catalog_resuslt = session.query(Catalog).all()
for catalog in catalog_resuslt:
	session.delete(catalog)
	session.commit()

item_result = session.query(Item).all()
for item in item_result:
	session.delete(item)
	session.commit()
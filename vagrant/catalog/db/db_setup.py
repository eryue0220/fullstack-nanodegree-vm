#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	passwd = Column(String(250), nullable=False)
	email = Column(String(80), nullable=False)


class Catalog(Base):
	__tablename__ = 'catalog'

	id = Column(Integer, autoincrement=True)
	name = Column(String(80), primary_key=True, nullable=False)

	@property
	def serialize(self):
		return {
			'name': self.name
		}


class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, autoincrement=True)
	name = Column(String(80), primary_key=True, nullable=False)
	description = Column(String(250))
	catalog_name = Column(String, ForeignKey('catalog.name'))
	catalog = relationship(Catalog)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'description': self.description
		}


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

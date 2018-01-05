#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from db_session import db_session
from db.db_setup import User


def get_user_id(email):
    try:
        user = db_session.query(User).filter_by(id=email).one()
        return user
    except:
        return None


def create_user(info):
    user = db_session.query(User).filter_by(email = info['email']).one_or_none()

    if user:
        return user.id

    new_user = User(
        email = info['email'],
        name = info['user_name']
    )

    db_session.add(new_user)
    db_session.commit()

    new_record = db_session.query(User).filter_by(email = info['email']).one()
    return new_record.id


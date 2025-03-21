#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.dog import Dog
from models.owner import Owner


def reset_database():
    Dog.drop_table()
    Owner.drop_table()
    Owner.create_table()
    Dog.create_table()


breakpoint()

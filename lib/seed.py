#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.dog import Dog
from models.owner import Owner


def seed_database():
    Dog.drop_table()
    Owner.drop_table()
    Owner.create_table()
    Dog.create_table()


    # Create seed data
    # owner = Owner.create("Nancy")
    # Dog.create("Fifi", 2, "Poodle", owner.id)


seed_database()
print("Seeded database")
# lib/models/dog.py
from models.__init__ import CURSOR, CONN
from models.owner import Owner

class Dog:
    all = {}

    def __init__(self, name, age, breed, owner_id, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.breed = breed
        self.owner_id = owner_id

    def __repr__(self):
        return (
                f"<Dog {self.id}: {self.name} {self.age} {self.breed}>" + 
                f"Owner ID: {self.owner_id}>"
            )
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )    
        
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if isinstance(age, int) and age > 0:
            self._age = age
        else:
            raise ValueError(
                "Age must be an integer greater than 0"
            )
        
    @property
    def breed(self):
        return self._breed

    @breed.setter
    def breed(self, breed):
        if isinstance(breed, str) and len(breed):
            self._breed = breed
        else:
            raise ValueError(
                "Breed must be a non-empty string"
            )
        
    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        if type(owner_id) is int and Owner.find_by_id(owner_id):
            self._owner_id = owner_id
        else:
            raise ValueError(
                "owner_id must reference a owner in the database")
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Dog instances """
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            breed TEXT,
            owner_id INTEGER,
            FOREIGN KEY (owner_id) REFERENCES owners(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Dog instances """
        sql = """
            DROP TABLE IF EXISTS dogs;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, and owner id values of the current Dog object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO dogs (name, age, breed, owner_id)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.age, self.breed, self.owner_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Dog instance."""
        sql = """
            UPDATE dogs
            SET name = ?, age = ?, breed = ?, owner_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.age, self.breed, self.owner_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Dog instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM dogs
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name, age, breed, owner_id):
        """ Initialize a new Dog instance and save the object to the database """
        dog = cls(name, age, breed, owner_id)
        dog.save()
        return dog
    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Dog object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        dog = cls.all.get(row[0])
        if dog:
            # ensure attributes match row values in case local instance was modified
            dog.name = row[1]
            dog.age = row[2]
            dog.breed = row[3]
            dog.owner_id = row[4]
        else:
            # not in dictionary, create new instance and add to dictionary
            dog = cls(row[1], row[2], row[3], row[4])
            dog.id = row[0]
            cls.all[dog.id] = dog
        return dog
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Dog object per table row"""
        sql = """
            SELECT *
            FROM dogs
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_owner_id(cls, owner_id):
        sql = """
            SELECT * FROM dogs
            WHERE owner_id = ?
        """
        CURSOR.execute(sql, (owner_id,),)

        rows = CURSOR.fetchall()
        return [
            cls.instance_from_db(row) for row in rows
        ]
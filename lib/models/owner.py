# lib/models/owner.py
from models.__init__ import CURSOR, CONN


class Owner:
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Owner {self.id}: {self.name}>"
    
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
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Owner instances """
        sql = """
            CREATE TABLE IF NOT EXISTS owners (
            id INTEGER PRIMARY KEY,
            name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Owner instances """
        sql = """
            DROP TABLE IF EXISTS owners;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, and owner id values of the current Owner object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO owners (name)
                VALUES (?)
        """

        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Owner instance."""
        sql = """
            UPDATE owners
            SET name = ?,
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Owner instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM owners
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name):
        """ Initialize a new Owner instance and save the object to the database """
        owner = cls(name)
        owner.save()
        return owner
    
    @classmethod
    def instance_from_db(cls, row):
        """Return an Owner object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        owner = cls.all.get(row[0])
        if owner:
            # ensure attributes match row values in case local instance was modified
            owner.name = row[1]
        else:
            # not in dictionary, create new instance and add to dictionary
            owner = cls(row[1])
            owner.id = row[0]
            cls.all[owner.id] = owner
        return owner
    
    @classmethod
    def get_all(cls):
        """Return a list containing one Owner object per table row"""
        sql = """
            SELECT *
            FROM owners
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        """Return an Owner object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM owners
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def dogs(self):
        """Return list of dogs associated with current owner"""
        from models.dog import Dog

        return Dog.find_by_owner_id(self.id)

        # sql = """
        #     SELECT * FROM dogs
        #     WHERE owner_id = ?
        # """
        # CURSOR.execute(sql, (self.id,),)

        # rows = CURSOR.fetchall()
        # return [
        #     Dog.instance_from_db(row) for row in rows
        # ]
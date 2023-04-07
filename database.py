import csv
import os
from crypto import AES_Cipher
from firebase_functions import db

firebase_db = db.reference("data")


class Database:
    '''
        initialize the database instance
    '''
    def __init__(self, database_name) -> None:
        self.database_name = database_name
        self.appendStream = open(database_name, "a+")
        self.readStream = open(database_name, "r+")
        self.writer = csv.writer(self.appendStream, delimiter=",", lineterminator="\n")
        self.reader = csv.DictReader(
            self.readStream, delimiter=",", lineterminator="\n"
        )
        self.rows = [*self.reader]

    '''
        write a row to the database
    '''
    def write(self, row):

        if os.stat(self.database_name).st_size == 0:
            self.writer.writerow(row.keys())

        self.writer.writerow(row.values())
        print(self.writer)
        self.rows.append(row)
        self.appendStream.flush()
        firebase_db.push(row)

    '''
        prints all the rows in the database
    '''
    def show(self):
        print(self.rows)

    '''
        find operaton on the database, loops through all the encrypted data to find the matching row
    '''
    def find(self, primary_keys,config):
        print(primary_keys)
        for row in self.rows:
            if all(
                AES_Cipher.verify(details["data"], row[key], details["isEncrypted"])
                for key, details in primary_keys.items()
            ):
                return {
                    key: row[key]
                    if not config["form_fields"][key]["isEncrypted"]
                    else AES_Cipher.decrypt(row[key])
                    for key in row
                }
        data = firebase_db.get()
        for row in data:
            if all(
                AES_Cipher.verify(details["data"], row[key], details["isEncrypted"])
                for key, details in primary_keys.items()
            ):
                return {
                    key: row[key]
                    if not primary_keys[key]["isEncrypted"]
                    else AES_Cipher.decrypt(row[key])
                    for key in row
                }
        raise Exception("Row not found")

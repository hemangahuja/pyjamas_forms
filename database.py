import csv,os
from crypto import verify

class Database():
    def __init__(self,database_name) -> None:
        self.database_name = database_name
        self.appendStream = open(database_name, "a+")
        self.readStream = open(database_name, "r+")
        self.writer = csv.writer(self.appendStream, delimiter=",", lineterminator="\n")
        self.reader = csv.DictReader(self.readStream, delimiter=",", lineterminator="\n")
        self.rows = [*self.reader]

    def write(self,row):
        print(row)

        if os.stat(self.database_name).st_size == 0:
            self.writer.writerow(row.keys())
        
        self.writer.writerow(row.values())
        print(self.writer)
        self.rows.append(row)
        self.appendStream.flush()

    def show(self):
        print(self.rows)

    def find(self,primary_keys):
        # print("primary keys",primary_keys.items())
        for row in self.rows:
            if all(verify(details['data'],row[key],details['isEncrypted']) for key,details in primary_keys.items()):
                return {key : row[key] for key in row if not key in primary_keys or not primary_keys[key]['isEncrypted']}
        raise Exception("Row not found")
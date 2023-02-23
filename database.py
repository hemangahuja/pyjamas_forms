import csv,os

class Database():
    def __init__(self,database_name) -> None:
        self.database_name = database_name
        self.writer = csv.writer(open(database_name, "a+"), delimiter=",", lineterminator="\n")
        self.reader = csv.reader(open(database_name, "r+"), delimiter=",", lineterminator="\n")

    def write(self,row):
        if os.stat(self.database_name).st_size == 0:
            self.writer.writerow(row.keys())
        
        self.writer.writerow(row.values())


import mysql.connector as sql
import json
import argparse

class Connect:
    @staticmethod
    def connection():

        try:
            connection = sql.connect(host = "localhost",
                                     user = "root",
                                     password = "JewelGote@2021",
                                     db = "project0"
                                    )
            
            cursor = connection.cursor()
            return [connection, cursor]

        
        except Exception as e:
            print(e)



class Queries:

    # parameterized constructor
    def __init__(self, connection, cursor):
        self.curs = cursor
        self.conn = connection

    def setup(self):
        jsonconfig = json.load(open('classes.json', 'r'))
        for schema in jsonconfig['schemas']:
            tablename = schema['tablename']
            checkstmt = f"SHOW TABLES LIKE '{tablename}'"
            self.curs.execute(checkstmt)
            result = self.curs.fetchone()
            if result:
                continue
            executestring = f"CREATE TABLE {tablename} ("
            insertstring = f"INSERT INTO TABLE {tablename} ("
            for column in schema['columns']:
                executestring += f"{column[0]} {column[1]}, "
                if column[1] == "INT NOT NULL AUTO_INCREMENT":
                    continue
                insertstring += f"{column[0]}, "
            # strip the trailing comma and space from the generated string
            if schema['primarykey'] is not None:
                executestring = executestring + f"PRIMARY KEY ({schema['primarykey']}));"
            else: 
                executestring = executestring[:-2] + ");"
            insertstring = insertstring[:-2] + ") VALUES ("
            # print(executestring)
            self.curs.execute(executestring)
            if schema['data'] is not None:
                for item in schema['data']:
                    funnystring = insertstring
                    for value in item.values():
                        funnystring += f"{value}, "
                    self.curs.execute(funnystring[:-2]+");")
            print("Tables created and populated (when applicable)")

connectList = Connect.connection()
# obj = Queries(connectList[0], connectList[1])
# obj.setup()

# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description='Placeholder')
parser.add_argument("--setup", default=False, action="store_true", help="Create the needed tables for the database.")

args = parser.parse_args()

queriesobj = Queries(connectList[0], connectList[1])

if args.setup:
    queriesobj.setup()
    exit(0)
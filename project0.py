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
            self.conn.commit()
            if schema['data'] is not None:
                for item in schema['data']:
                    funnystring = insertstring
                    for value in item.values():
                        funnystring += f"{value}, "
                    self.curs.execute(funnystring[:-2]+");")
                    self.conn.commit()
            print("Tables created and populated (when applicable)")

    def insert(self, tablename, values):
        insertstring = f"INSERT INTO {tablename} VALUES ("
        for value in values:
            insertstring += f"{value}, "
        insertstring = insertstring[:-2] + ");"
        self.curs.execute(insertstring)
        self.conn.commit()

    def get_class(self, classname):
        self.curs.execute(f"SELECT * FROM classes WHERE name={classname};")
        result = self.curs.fetchone()
        return result

    def add_enemy(self, name, health, attack):
        enemy = f"{name}, {health}, {attack}"
        self.curs.execute(f"INSERT INTO enemies VALUES ({enemy});")
        self.conn.commit()
    
    def get_all_rows(self, tablename):
        self.curs.execute(f"SELECT * FROM {tablename};")
        result = self.curs.fetchall()
        return result

    def get_row_by_id(self, tablename, id):
        self.curs.execute(f"SELECT * FROM {tablename} WHERE id={id};")
        result = self.curs.fetchone()
        return result

class Game:
    # create the constructor for the class

    def __init__(self, connection, cursor):
        self.curs = cursor
        self.conn = connection

    # ask the player for what class they want to play
    
    # Will most likely need to be cleaned
    def welcome():
        print("Welcome!\n")
        print("Please pick a character to get started\n")
        print("Rock[1], Paper[2], Scissors [3]\n")
        choice = input()

        if (choice ==1):
            # placeholder
            return 0
        elif(choice == 2):
            return 0

        elif(choice == 3):
            return 0


    # possibly in a while loop, run through the game

    def gameRun():
        dead = False
        # while dead == False:


    # fetching data from the tables during an enemy encounter to produce an enemy

connectList = Connect.connection()
# obj = Queries(connectList[0], connectList[1])
# obj.setup()

# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description='Placeholder')
parser.add_argument("--setup", default=False, action="store_true", help="Create the needed tables for the database.")
parser.add_argument("--insert", default=False, action="store_true", help="Insert generic data into the database. (Mainly for debugging)")
parser.add_argument("--enemy", default=False, action="store_true", help="Insert an enemy into the database.")


args = parser.parse_args()

queriesobj = Queries(connectList[0], connectList[1])

if args.setup:
    queriesobj.setup()
    exit(0)





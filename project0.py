import mysql.connector as sql
import json
import argparse
import tableprint as tp
import random

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
            insertstring = f"INSERT INTO {tablename} ("
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
                funnystrings = []
                for item in schema['data']:
                    funnystring = insertstring
                    for value in item.values():
                        if type(value) == str:
                            funnystring += f"'{value}', "
                        else:
                            funnystring += f"{value}, "
                    funnystring = funnystring[:-2] + ");"
                    # print(funnystring)
                    funnystrings.append(funnystring)
                # print(funnystrings)
                for funnystring in funnystrings:
                    self.curs.execute(funnystring)
            print("Tables created and populated (when applicable)")
            self.conn.commit()

    def insert(self, tablename, values):
        insertstring = f"INSERT INTO {tablename} VALUES ("
        for value in values:
            if type(value) == str:
                insertstring += f"'{value}', "
            else:
                insertstring += f"{value}, "
        insertstring = insertstring[:-2] + ");"
        self.curs.execute(insertstring)
        self.conn.commit()

    def get_class(self, classname):
        self.curs.execute(f"SELECT * FROM classes WHERE name='{classname}';")
        result = self.curs.fetchone()
        return result

    def add_enemy(self, name, health, attack):
        enemy = f"'{name}', {health}, {attack}"
        self.curs.execute(f"INSERT INTO enemydata (name, health, attack) VALUES ({enemy});")
        self.conn.commit()
    
    def get_all_rows(self, tablename):
        self.curs.execute(f"SELECT * FROM {tablename};")
        result = self.curs.fetchall()
        return result

    def get_row_by_id(self, tablename, id):
        self.curs.execute(f"SELECT * FROM {tablename} WHERE id={id};")
        result = self.curs.fetchone()
        return result
    
    def describe_table(self, tablename):
        self.curs.execute(f"DESCRIBE {tablename};")
        result = self.curs.fetchall()
        return result

    def add_player(self, name, health, attack):
        player = f"'{name}', {health}, {attack}"
        self.curs.execute(f"INSERT INTO playerdata (class, health, attack) VALUES ({player});")
        self.conn.commit()
    
    def get_row_amount(self, tablename):
        self.curs.execute(f"SELECT COUNT(*) FROM {tablename};")
        result = self.curs.fetchone()
        return result[0]
    
    def update_value(self, tablename, column, value):
        if type(value) == str:
            value = f"'{value}'"
        self.curs.execute(f"UPDATE {tablename} SET {column} = {value};")
        self.conn.commit()
    
    def delete_row(self, tablename, id):
        self.curs.execute(f"DELETE FROM {tablename} WHERE id={id};")
        self.conn.commit()

class Game:
    # create the constructor for the class

    def __init__(self, connection, cursor):
        self.curs = cursor
        self.conn = connection
        self.queries = Queries(connection, cursor)

    # ask the player for what class they want to play
    
    # Will most likely need to be cleaned
    def player_setup(self):
        print("Please pick a character to get started")
        classes = self.queries.get_all_rows("classes")
        columns = self.queries.describe_table("classes")
        # print(classes)
        tableheaders = []
        for column in columns:
            tableheaders.append(column[0])
        tp.table(classes, tableheaders)
        classnames= []
        for class_ in classes:
            classnames.append(class_[0])
        class_choice = input("What class would you like to play? ")
        if class_choice not in classnames:
            print("That is not a valid class")
            return self.player_setup()
        player_class = self.queries.get_class(class_choice)
        self.queries.add_player(player_class[0], player_class[2], player_class[3])
        print("You have chosen to play as a " + player_class[0])

    # possibly in a while loop, run through the game

    def gameRun(self):
        hp = self.queries.get_row_by_id("playerdata", 1)[2]
        attack = self.queries.get_row_by_id("playerdata", 1)[3]
        enemycount = self.queries.get_row_amount("enemydata")
        while hp > 0:
            # game stuff here
            enemy = self.queries.get_row_by_id("enemydata", random.randint(1, enemycount))
            enemyhp = enemy[2]
            print("You have encountered " + enemy[1])
            if hp <= 0:
                print("You have died")
                break
            print("Your health is " + str(hp))
            print("Your enemy's health is " + str(enemyhp))
            while enemyhp > 0:
                if hp <= 0:
                    break
                print("What would you like to do?")
                print("1. Attack")
                print("2. Heal")
                print("3. Buff")
                print("4. Quit")
                choice = input("What would you like to do? ")
                if choice == "1":
                    print("You attacked the enemy")
                    enemyhp -= self.queries.get_row_by_id("playerdata", 1)[3]
                    hp -= enemy[3]
                    print("Your enemy's health is " + str(enemyhp))
                elif choice == "2":
                    print("You healed")
                    hp += random.randint(1, 10)
                    print("Your health is " + str(hp))
                elif choice == "3":
                    print("You buffed")
                    attack += random.randint(1, 10)
                    self.queries.update_value("playerdata", "attack", attack)
                    print("Your attack is " + str(attack))
                elif choice == "4":
                    print("You quit the game")
                    self.queries.update_value("playerdata", "health", hp)
                    self.queries.update_value("playerdata", "attack", attack)
                    exit(0)
                else:
                    print("That is not a valid choice")
                print("The enemy attacks you")
                hp -= enemy[3]
                print("Your health is " + str(hp))
            print("You have defeated the enemy")
        print("You have died")
        print("Game Over")
        self.queries.delete_row("playerdata", 1)
        


    # fetching data from the tables during an enemy encounter to produce an enemy

connectList = Connect.connection()
# obj = Queries(connectList[0], connectList[1])
# obj.setup()

# https://docs.python.org/3/library/argparse.html
parser = argparse.ArgumentParser(description='Placeholder')
parser.add_argument("--setup", default=False, action="store_true", help="Create the needed tables for the database.")
#parser.add_argument("--insert", default=False, action="store_true", help="Insert generic data into the database. (Mainly for debugging)")
parser.add_argument("--enemy", default=False, action="store_true", help="Insert an enemy into the database.")
parser.add_argument("--enemy-name", default=False, help="Name of the enemy to insert.")
parser.add_argument("--enemy-health", default=False, help="Health of the enemy to insert.")
parser.add_argument("--enemy-attack", default=False, help="Attack of the enemy to insert.")
parser.add_argument("-s", "--start", default=False, action="store_true", help="Start the game.")

args = parser.parse_args()

queriesobj = Queries(connectList[0], connectList[1])

if args.start:
    game = Game(connectList[0], connectList[1])
    if queriesobj.get_row_amount("playerdata") == 0:
        game.player_setup()
    game.gameRun()

if args.setup:
    queriesobj.setup()
    exit(0)

if args.enemy:
    if args.enemy_name and args.enemy_health and args.enemy_attack:
        queriesobj.add_enemy(args.enemy_name, args.enemy_health, args.enemy_attack)
    else:
        print("Please provide a name, health, and attack value.")
        exit(1)
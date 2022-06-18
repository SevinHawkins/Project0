import mysql.connector as sql
import json

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

        
        except sql.Error as e:
            print(e)




class Queries:

    # parameterized constructor
    def __init__(self, connection, cursor):
        self.curs = cursor
        self.conn = connection

    def setup(self):
        schema = json.load(open('classes.json', 'r'))
        tablename = schema['tablename']
        executestring = f"CREATE TABLE {tablename} ("
        for column in schema['columns']:
            executestring += column + ", "
        # strip the trailing comma and space from the generated string
        executestring = executestring[:-2] + ");"
        self.curs.execute(executestring)


connectList = Connect.connection()
obj = Queries(connectList[0], connectList[1])
obj.setup()
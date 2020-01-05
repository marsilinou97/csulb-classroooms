import psycopg2
from threading import Lock


class Singleton:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self


class connector:
    con = False
    insert_lock = Lock()
    rooms = dict()
    cursor = None

    @staticmethod
    def make_connection():
        if not connector.con:
            print("Making connection...")
            try:
                connector.connection = psycopg2.connect(user="rikwjbvg",
                                                        password="PTmEK_y0-uyC3kRIbWwLlihyUQZYUtA-",
                                                        host="salt.db.elephantsql.com",
                                                        port="5432",
                                                        database="rikwjbvg")

                connector.cursor = connector.connection.cursor()
                connector.con = True
                connector.rooms = connector.__get_all_rooms()
            except Exception as e:
                print(e)

    @staticmethod
    def __get_all_rooms():
        print("Getting all rooms")
        connector.cursor.execute(f'''
                           SELECT ID, BUILDING, ROOM_NUM
                            FROM RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS
                            ORDER BY ID
                            ''')
        rooms = {f"{building}-{room}": room_id for room_id, building, room in connector.cursor.fetchall()}
        return rooms

    @staticmethod
    def get_rooms():
        return connector.rooms

    @staticmethod
    def inset_room(room):
        with connector.insert_lock:
            # Check if a different thread added the room
            if "-".join(room) in connector.rooms.keys():
                return connector.rooms["-".join(room)]
            print(f"Inserting room {room}")
            query = """INSERT INTO RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS(building, room_num) VALUES (%s, %s)"""
            connector.cursor.execute(query, tuple(room))
            connector.connection.commit()
            query = """SELECT id FROM RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS WHERE building = %s AND room_num = %s"""
            connector.cursor.execute(query, tuple(room))
            res = connector.cursor.fetchone()
            connector.rooms["-".join(room)] = res
            print(f"Room inserted correctly")
            return res[0]

    @staticmethod
    def close_conn():
        connector.connection.commit()
        connector.cursor.close()
        connector.connection.close()

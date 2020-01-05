import psycopg2
from threading import Lock
import os

class connector:
    con = False
    insert_lock = Lock()
    rooms = None
    cursor = None

    @staticmethod
    def make_connection():
        if not connector.con:
            print("Making connection...")
            try:
                connector.connection = psycopg2.connect(user="rikwjbvg",
                                                        password=os.environ.get("DB_PASSWORD"),
                                                        host="salt.db.elephantsql.com",
                                                        port="5432",
                                                        database="rikwjbvg")
                connector.cursor = connector.connection.cursor()
                connector.con = True
            except Exception as e:
                print(e)

    @staticmethod
    def __get_all_rooms():
        print("Getting all rooms")
        if not connector.cursor:
            connector.make_connection()
        connector.cursor.execute(f'''
                           SELECT ID, BUILDING, ROOM_NUM
                            FROM RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS
                            ORDER BY ID
                            ''')
        connector.rooms = {f"{building}-{room}": room_id for room_id, building, room in connector.cursor.fetchall()}
        return connector.rooms

    @staticmethod
    def get_rooms():
        if not connector.rooms:
            connector.__get_all_rooms()
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
    def insert_courses_info():
        try:
            if not connector.cursor:
                connector.make_connection()
            query = "INSERT INTO MAIN_APP_CLASSESINFO (class_number, class_days, start_time, end_time, class_comments, instructor, building, room_num, class_type, course_title) VALUES"
            for x in os.listdir('sql_queries'):
                with open(f"sql_queries/{x}") as f:
                    query += f.read()
            query = query[:-1] + ";"
            connector.cursor.execute(query)
        except Exception as error:
            print("Error while creating PostgreSQL: ", error)
        finally:
            connector.close_conn()

    @staticmethod
    def execute_query(q):
        if not connector.cursor:
            connector.make_connection()
        connector.cursor.execute(q)
        connector.close_conn()

    @staticmethod
    def close_conn():
        connector.connection.commit()
        connector.cursor.close()
        connector.connection.close()

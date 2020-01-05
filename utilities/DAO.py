from django.db import connection


class database_access_object(object):
    def __init__(self, arg):
        self.cursor = connection.cursor()

    def get_abbreviations(self):
        self.cursor.execute(f'''
                           SELECT DISTINCT BUILDING 
                            FROM RIKWJBVG.PUBLIC.CLASSES
                            ''')

    def get_rooms(self, start_time='', end_time='', day='', room_number='', building=''):
        pass

    def get_all_rooms(self):
        self.cursor.execute(f'''
                           SELECT ID, ROOM_NUM, BUILDING
                            FROM RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS
                            ORDER BY ID
                            ''')
        return self.cursor.fetchall()


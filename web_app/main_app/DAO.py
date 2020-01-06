from django.db import connection


# from . models import ClassesInfo

class database_access_object(object):
    def __init__(self):
        self.curr = connection.cursor()

    def get_buildings(self):
        c = self.curr.execute(f'''
                        SELECT DISTINCT building
                            FROM main_app_classrooms 
                            WHERE building NOT IN ('TBA', 'ONLINE')
                            ORDER BY building
                            ''')
        return self.curr.fetchall()

    def get_rooms(self, start_time='%', end_time='%', day='%', room_number='%', building='%'):
        print(f'''                        SELECT R.building || ' ' || R.room_num
                        FROM MAIN_APP_CLASSROOMS R
                        WHERE NOT exists
                            (
                                SELECT 1
                                FROM MAIN_APP_CLASSESINFO C
                                WHERE C.ROOM_NUM = R.ID
                                  AND TO_TIMESTAMP(C.START_TIME, 'HH24:MI:SS')::TIME < '{end_time}'::TIME
                                  AND TO_TIMESTAMP(C.END_TIME, 'HH24:MI:SS')::TIME > '{start_time}'::TIME
                                  AND C.CLASS_DAYS LIKE '%{day}%'
                            )
                          AND BUILDING = '{building}';''')

        c = self.curr.execute(f'''
                        SELECT R.building || ' ' || R.room_num
                        FROM MAIN_APP_CLASSROOMS R
                        WHERE NOT exists
                            (
                                SELECT 1
                                FROM MAIN_APP_CLASSESINFO C
                                WHERE C.ROOM_NUM = R.ID
                                  AND TO_TIMESTAMP(C.START_TIME, 'HH24:MI:SS')::TIME < '{end_time}'::TIME
                                  AND TO_TIMESTAMP(C.END_TIME, 'HH24:MI:SS')::TIME > '{start_time}'::TIME
                                  AND C.CLASS_DAYS LIKE '%{day}%'
                            )
                          AND BUILDING = '{building}'
                        ORDER BY room_num;
                            ''')
        res = self.curr.fetchall()
        print("\n\n\n")
        print(res)
        return res

from django.db import connection
# from . models import ClassesInfo

class database_access_object(object):
    def __init__(self):
        self.curr = connection.cursor()

    def get_buildings(self):
        c = self.curr.execute(f'''
                        SELECT DISTINCT building 
                            FROM MAIN_APP_CLASSESINFO
                            ORDER BY building
                            ''')
        return self.curr.fetchall()


    def get_rooms(self, start_time='', end_time='', day='', room_number='', building=''):
        c = self.curr.execute(f'''
                    SELECT building || '-' || room_num
                    FROM MAIN_APP_CLASSESINFO R
                    WHERE NOT exists
                        (
                            SELECT 1
                            FROM MAIN_APP_CLASSESINFO C
                            WHERE C.id = R.ID
                              AND TO_TIMESTAMP(C.start_time, 'HH24')::TIME < '{end_time}'::TIME
                              AND TO_TIMESTAMP(C.end_time, 'HH24')::TIME > '{start_time}'::TIME
                              AND C.class_days LIKE '%{day}%'
                        )
                      AND room_num LIKE '%{room_number}'
                      AND building = '{building}'
                    ORDER BY building || '-' || room_num;
                            ''')
        print(f'''
                    SELECT building || '-' || room_num
                    FROM MAIN_APP_CLASSESINFO R
                    WHERE NOT exists
                        (
                            SELECT 1
                            FROM MAIN_APP_CLASSESINFO C
                            WHERE C.id = R.ID
                              AND TO_TIMESTAMP(C.start_time, 'HH24')::TIME < '{end_time}'::TIME
                              AND TO_TIMESTAMP(C.end_time, 'HH24')::TIME > '{start_time}'::TIME
                              AND C.class_days LIKE '%{day}%'
                        )
                      AND room_num LIKE '%{room_number}'
                      AND building = '{building}'
                    ORDER BY building || '-' || room_num;
                            ''')
        res = self.curr.fetchall()
        print(len(res))
        return res

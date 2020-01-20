from django.db import connection


class database_access_object(object):
    def __init__(self):
        pass

    def execute_query(self, query, parameters=None):
        with connection.cursor() as curr:
            curr.execute(query, parameters)
            return curr.fetchall()

    def get_buildings(self):
        query = (f'''
                        SELECT DISTINCT BUILDING
                            FROM MAIN_APP_CLASSROOMS 
                            WHERE BUILDING NOT IN ('TBA', 'ONLINE')
                            ORDER BY BUILDING
                            ''')
        return self.execute_query(query)

    def get_rooms(self, start_time=None, end_time=None, day=None, room_number=None, building=None):
        parameters = dict(start_time=start_time, end_time=end_time, day=day, room_number=room_number, building=building)
        query = ('''
                                SELECT DISTINCT R.BUILDING || ' ' || R.ROOM_NUM
                                FROM MAIN_APP_CLASSROOMS R
                                         INNER JOIN MAIN_APP_CLASSESINFO C ON C.ROOM_NUM = R.ID
                                WHERE START_TIME IS NOT NULL
                                  AND NOT EXISTS
                                    (SELECT NULL
                                     FROM MAIN_APP_CLASSESINFO C2
                                     WHERE C2.ROOM_NUM = R.ID
                                       AND C2.START_TIME  > %(start_time)s :: TIME
                                       AND C2.START_TIME  < %(end_time)s :: TIME
                                       AND R.ROOM_NUM LIKE %(room_number)s)
                                  AND CLASS_DAYS LIKE %(day)s
                                  AND BUILDING = %(building)s
                                  AND R.ROOM_NUM LIKE %(room_number)s;
                ''')
        return self.execute_query(query, parameters)

    def get_specific_room(self, room_number, building):
        parameters = dict(room_number=room_number, building=building)
        query = """
                SELECT START_TIME || ' - ' || END_TIME
                FROM (
                         SELECT '06:00:00'::TIME START_TIME, min(START_TIME) END_TIME
                         FROM MAIN_APP_CLASSESINFO
                         WHERE ROOM_NUM = 71
                         UNION ALL
                         SELECT END_TIME, lead(START_TIME) OVER (ORDER BY START_TIME)
                         FROM MAIN_APP_CLASSESINFO
                         WHERE ROOM_NUM = 71
                         UNION ALL
                         SELECT max(END_TIME), '23:59:59'::TIME
                         FROM MAIN_APP_CLASSESINFO
                         WHERE ROOM_NUM = 71
                     ) T
                WHERE START_TIME <> END_TIME;
                """
        self.execute_query(query, parameters)

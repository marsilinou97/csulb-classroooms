# import os
# import psycopg2
# import time
#
#
# def connect():
#     try:
#         connection = psycopg2.connect(user="rikwjbvg",
#                                       password="PTmEK_y0-uyC3kRIbWwLlihyUQZYUtA-",
#                                       host="salt.db.elephantsql.com",
#                                       port="5432",
#                                       database="rikwjbvg")
#
#         cursor = connection.cursor()
#         # q = "INSERT INTO MAIN_APP_CLASSESINFO (class_number, class_days, start_time, end_time, class_comments, instructor, building, room_num, class_type, course_title) VALUES"
#         q = "INSERT INTO MAIN_APP_CLASSESINFO (class_number, class_days, start_time, end_time, class_comments, instructor, building, room_num, class_type, course_title) VALUES"
#         for x in os.listdir('sql_queries'):
#             with open(f"sql_queries/{x}") as f:
#                 q += f.read()
#         query = q[:-1] + ";"
#         # print(query)
#         cursor.execute(query)
#
#     except (Exception, psycopg2.DatabaseError) as error:
#         print("Error while creating PostgreSQL: ", error)
#     finally:
#         # closing database connection.
#         if (connection):
#             connection.commit()
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
#
#
# if __name__ == '__main__':
#     start = time.time()
#     connect()
#     print(f"Time of execution: {time.time() - start}")
#

from requests_html import HTMLSession
import psycopg2

session = HTMLSession()
url = "https://www.csulb.edu/academic-technology-services/classroom-support-services/classroom-types-room"
resp = session.get(url).html
rooms = [room.text.split("-") for room in resp.find("tbody tr th")]
query = """INSERT INTO RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS(building, room_num) VALUES """
connection = psycopg2.connect(user="rikwjbvg",
                              password="PTmEK_y0-uyC3kRIbWwLlihyUQZYUtA-",
                              host="salt.db.elephantsql.com",
                              port="5432",
                              database="rikwjbvg")

cursor = connection.cursor()

rooms_tuple = [tuple(room) for room in rooms]

for room in list(set(rooms_tuple)):
    query += str(tuple(room)) + ", "

cursor.execute(query[:-2])
print(f"Added all rooms")

connection.commit()
cursor.close()
connection.close()

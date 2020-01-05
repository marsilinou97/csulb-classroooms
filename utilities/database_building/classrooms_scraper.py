from requests_html import HTMLSession
from helper_methods import connector as con
import psycopg2

session = HTMLSession()
url = "https://www.csulb.edu/academic-technology-services/classroom-support-services/classroom-types-room"
resp = session.get(url).html
rooms = [room.text.split("-") for room in resp.find("tbody tr th")]
query = """INSERT INTO RIKWJBVG.PUBLIC.MAIN_APP_CLASSROOMS(building, room_num) VALUES """

rooms_tuple = [tuple(room) for room in rooms]

for room in list(set(rooms_tuple)):
    query += str(tuple(room)) + ", "

con.execute_query(query[:-2])
print(f"Added all rooms")
con.close_conn()

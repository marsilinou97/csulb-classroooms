import concurrent.futures as cf
from requests_html import HTMLSession
import time
import datetime
from dao_test import connector as con
import sys, os
from threading import Lock
insert_room_lock = Lock()
# con = connector()
THREADS = 25
con.make_connection()
# rooms = con.get_rooms()
session = HTMLSession()


def parse_time(text):
    pm = None  # unknown

    if text[-2:] in ('AM', 'PM'):
        pm = (text[-2:] == 'PM')
        text = text[:-2]

    if ':' not in text:
        text += ':00'

    hours, minutes = text.split(':')
    hours = int(hours)
    minutes = int(minutes)

    if pm and hours < 12:
        hours += 12

    return datetime.time(hours, minutes), pm is not None


def parse_interval(text):
    if 'TBA' in text:
        return None, None

    start, end = text.split('-')

    start, is_exact = parse_time(start)
    end, _ = parse_time(end)  # end time should be exact

    # If both the start and end times are known then there's nothing left to do
    if is_exact:
        return start, end

    # start2 = start + 12 hours
    start2 = start.replace(hour=(start.hour + 12) % 24)
    start_AM, start_PM = sorted([start, start2])

    # Pick the most reasonable option
    if start_AM < end < start_PM:
        return start_AM, end
    elif start_AM < start_PM < end:
        return start_PM, end
    else:
        raise ValueError('This cannot happen')


def parse_build_room(br):
    try:
        if br in con.rooms.keys():
            return con.rooms[br]
        if "-" in br:
            temp_room = br.split("-")[:2]
        else:
            temp_room = [br, br]
        with insert_room_lock:
            room_id = con.inset_room(temp_room)
            con.rooms["-".join(temp_room)] = room_id
            return room_id
    except Exception as e:
        print(f"Error in parse building: {e}, br: {br=}")


def subject_parser(subject):
    subject_url = f"http://web.csulb.edu/depts/enrollment/registration/class_schedule/Fall_2018/By_Subject/{subject}"
    query = ""
    empty = True
    try:
        subject_soup = session.get(subject_url).html
        course_block = subject_soup.find(".session .courseBlock")
        print(f"{subject_url=}")
        for section in course_block:
            title = section.find(".courseTitle", first=True).text
            title = title.replace("'", "''")
            for course_row in section.find(".sectionTable tr:not(:first-child)")[:]:
                class_info = [x.text for x in course_row.find("td")]
                class_info = [x.replace("'", "''") for x in class_info]
                start_time, end_time = parse_interval(class_info[6])
                room_id = parse_build_room(class_info[8])
                query += f"( '{class_info[0]}', '{class_info[5]}', '{start_time}', '{end_time}', '{class_info[10]}', '{class_info[9]}', NULL, '{room_id}', '{class_info[4]}', '{title}'),"
                empty = False
        if not empty:
            with open(f"sql_queries/{subject.split('.')[0]}.sql", "w") as f:
                f.write(query)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(f"Error: {e}\nError subject: {subject}, room_id: {room_id}")


def main():
    try:
        con.make_connection()
        # Find all subjects' links
        resp = session.get(
            "http://web.csulb.edu/depts/enrollment/registration/class_schedule/Fall_2019/By_Subject/").html
        subjects = [list(subject.find('a', first=True).links)[0] for subject in resp.find("#pageContent li")]
        start = time.time()
        with cf.ThreadPoolExecutor(THREADS) as ex:
            ex.map(subject_parser, sorted(subjects[:]))
        con.close_conn()
        print(f"Time of execution: {time.time() - start}")
    except Exception as e:
        print(f"Main Error: {e}")


if __name__ == '__main__':
    main()

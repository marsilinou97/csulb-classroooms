import concurrent.futures as cf
import shutil, os
from requests_html import HTMLSession
import time
import datetime

session = HTMLSession()
# Find all subjects' links
resp = session.get("http://web.csulb.edu/depts/enrollment/registration/class_schedule/Fall_2019/By_Subject/").html
subjects = [subject.find('a', first=True).links for subject in resp.find("#pageContent li")]


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
    if "-" in br:
        return br.split("-")
    else:
        return [br, br]


def subject_parser(subject):
    subject = list(subject)[0]
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
                building, room = parse_build_room(class_info[8])
                query += f"( '{class_info[0]}', '{class_info[5]}', '{start_time}', '{end_time}', '{class_info[10]}', '{class_info[9]}', '{room_id}', '{class_info[4]}', '{title}'),"
                # query += f"( '{class_info[0]}', '{class_info[5]}', '{start_time}', '{end_time}', '{class_info[10]}', '{class_info[9]}', '{building}', '{room}', '{class_info[4]}', '{title}'),"
                empty = False
        if not empty:
            with open(f"sql_queries/{subject.split('.')[0]}.sql", "w") as f :
                f.write(query)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    start = time.time()
    with cf.ProcessPoolExecutor() as ex:
        ex.map(subject_parser, sorted(subjects[:]))
    print(f"Time of execution: {time.time() - start}")

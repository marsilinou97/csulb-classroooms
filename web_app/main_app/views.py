from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
import re
from . import DAO
from .forms import QueryForm

connector = DAO.database_access_object()
global BUILDINGS
BUILDINGS = connector.get_buildings()
WEEK_DAYS = {'Monday': 'M', 'Tuesday': 'Tu', 'Wednesday': 'W', 'Thursday': 'Th', 'Friday': 'F'}


def handle_post_request(request, form):
    global WEEK_DAYS, BUILDINGS
    current_datetime = datetime.now()

    # Set get form values
    values = dict()
    values['start_time'] = form.cleaned_data['start_time']
    values['end_time'] = form.cleaned_data['end_time']
    values['day'] = form.cleaned_data['day']
    values['room_number'] = form.cleaned_data['room_number']
    values['building'] = form.cleaned_data['building']
    values['message'] = ''

    # Validate start and end times
    pattern = re.compile(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9]$')
    if not (pattern.match(values['start_time']) and pattern.match(values['end_time'])):
        # Time given is not a correct time format (hh:mm) reset time to 8AM
        values['start_time'] = '08:00'  # current_datetime.strftime("%I:%M%p")
        values['end_time'] = '08:30'  # (current_datetime + timedelta(minutes=30)).strftime("%I:%M%p")
        values['message'] += 'Time badly formatted, new start time is set to 8AM and end time is set to 8:30AM\n'
    else:
        # Validate time range (Deny any request after 12:00AM)
        temp_start_time = values['start_time'].split(":")
        temp_end_time = values['end_time'].split(":")
        # Verify that end time is greater than start time
        if current_datetime.replace(hour=temp_start_time[0], minute=temp_start_time[1]) > current_datetime.replace(hour=temp_end_time[0], minute=temp_end_time[1]):
            values['start_time'], values['start_time'] = values['start_time'], values['start_time']
            values['message'] += "Start time can't be greater than end time, times are swapped!\n"
        # End time must be before 12AM
        if int(temp_end_time[0]) > 12:
            values['message'] += "End time must be before 12AM, " \
                                 "new start time is set to 8AM and end time is set to 8:30AM!\n"
            values['start_time'] = '08:00'
            values['end_time'] = '08:30'

    # Validate day is a weekday
    if values['day'] not in WEEK_DAYS.values():
        # Set day to today's day if it's not a weekend
        if WEEK_DAYS[current_datetime.strftime('%A')] not in ['St', 'Su']:
            values['message'] += "Invalid day was given, setting day to Today instead!\n"
            values['day'] = WEEK_DAYS[current_datetime.strftime('%A')]
        # Set day to Monday if today is a weekend
        else:
            values['message'] += "Invalid day was given, setting day to Monday instead!\n"
            values['day'] = 'M'

    # Handle empty room number
    if not values['room_number']:
        values['room_number'] = '%'

    results = connector.get_rooms(start_time=values['start_time'],
                                  end_time=values['end_time'],
                                  day=values['day'],
                                  room_number=values['room_number'],
                                  building=values['building']
                                  )

    render(request, 'web_app/results_table.html', {'schedule': results})
    return render(request, 'web_app/form.html', {
        'schedule': results,
        'buildings': BUILDINGS,
        'resultsCount': len(results),
        'days': WEEK_DAYS,
        'building': BUILDINGS,
        'results': True})


def handle_get_request(request, message=None):
    global WEEK_DAYS, BUILDINGS
    return render(request, 'web_app/form.html',
                  {
                      'buildings': BUILDINGS,
                      'days': WEEK_DAYS,
                      'message': message
                  })


def index(request):
    # Handle post requests
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            return handle_post_request(request, form)
        else:
            error_message = 'There was an error in your form submission, Fill all required fields with valid data!'
            return handle_get_request(request, error_message)
    elif request.method == 'GET':
        return handle_get_request(request)
    # If requests received is not GET or POST (ie. PUT or DELETE, ect...) then redirect to the main page
    else:
        return HttpResponse('<h1>Error!</h1>')


def feedback(request):
    return render(request, 'web_app/feedback.html')
    # TODO: Build feedback page


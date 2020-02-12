import logging
import re
from datetime import datetime
from datetime import timedelta

from django import forms
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from tracking.models import Visitor, Pageview
from tracking.settings import TRACK_PAGEVIEWS

from . import DAO
from .forms import QueryForm

# Set global variables
CONNECTOR = DAO.DatabaseAccessObject()
global BUILDINGS, TIME_PATTERN
BUILDINGS = CONNECTOR.get_buildings()
WEEK_DAYS = {'Monday': 'M', 'Tuesday': 'Tu', 'Wednesday': 'W', 'Thursday': 'Th', 'Friday': 'F'}
TIME_PATTERN = re.compile(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9]):[0-5][0-9]$')
CURRENT_DATETIME = datetime.now()


def validate_day(day):
    message = ''
    # Validate day is a weekday
    if day not in WEEK_DAYS.keys():
        # Set day to today's day if it's not a weekend
        if CURRENT_DATETIME.strftime('%A') not in ['Saturday', 'Sunday']:
            message = "- Invalid day was given, setting day to Today instead!"
            day = WEEK_DAYS[CURRENT_DATETIME.strftime('%A')]
        # Set day to Monday if today is a weekend
        else:
            message = "- Invalid day was given, setting day to Monday instead!<br>"
            day = 'M'
    else:
        day = WEEK_DAYS[day]
    return day, message


def validate_time(start_time, end_time):
    message = ""
    print(start_time, end_time)
    if not (TIME_PATTERN.match(start_time) and TIME_PATTERN.match(end_time)):
        # Time given is not a correct time format (hh:mm) reset time to 8AM
        start_time = '08:00'  # current_datetime.strftime("%I:%M%p")
        end_time = '08:30'  # (current_datetime + timedelta(minutes=30)).strftime("%I:%M%p")
        message += '- Time badly formatted, new start time is set to 8AM and end time is set to 8:30AM<br>'
    else:
        # Validate time range (Deny any request after 12:00AM)
        temp_start_time = [int(i) for i in start_time.split(":")]
        temp_end_time = [int(i) for i in end_time.split(":")]
        # Verify that end time is greater than start time
        if CURRENT_DATETIME.replace(hour=temp_start_time[0], minute=temp_start_time[1]) > CURRENT_DATETIME.replace(
                hour=temp_end_time[0], minute=temp_end_time[1]):
            start_time, end_time = end_time, start_time
            message += "- Start time can't be greater than end time, times are swapped!<br>"
        # End time must be before 12AM
        if int(temp_end_time[0]) < 6 and int(temp_start_time[0]) >= 1:
            message += "- End time must be before 12AM, " \
                       "new start time is set to 8AM and end time is set to 8:30AM!<br>"
            start_time = '08:00'
            end_time = '08:30'
    return start_time, end_time, message


def get_form_dictionary(form):
    values = dict()
    values['message'] = ''
    values['start_time'] = form.cleaned_data['start_time']
    values['end_time'] = form.cleaned_data['end_time']

    validated_day = validate_day(form.cleaned_data['day'])
    values['day'] = validated_day[0]
    values['message'] += validated_day[1]

    values['room_number'] = form.cleaned_data['room_number']
    values['building'] = form.cleaned_data['building']
    return values


def option_one(request, values):
    print(values)
    results = CONNECTOR.get_specific_room(room_number=values['room_number'], building=values['building'],
                                          day=values['day'])
    render(request, 'web_app/results_table.html', {'schedule': results})

    return render(request, 'web_app/form.html', {
        'schedule': results,
        'buildings': BUILDINGS,
        'resultsCount': len(results),
        'days': WEEK_DAYS,
        'building': BUILDINGS,
        'message': values['message'],
        'results': True})


def option_two(request, values):
    print(f"Before: {values}")

    # Validate start and end times
    values['start_time'], values['end_time'], values['message'] = validate_time(values['start_time'],
                                                                                values['end_time'])

    # Handle empty room number
    if not values['room_number']:
        values['room_number'] = '%'
    print(f"After: {values}")
    results = CONNECTOR.get_rooms(start_time=values['start_time'],
                                  end_time=values['end_time'],
                                  day=values['day'],
                                  room_number=values['room_number'],
                                  building=values['building']
                                  )

    render(request, 'web_app/results_table.html', {'schedule': results})
    context = {
        'schedule': results,
        'buildings': BUILDINGS,
        'resultsCount': len(results),
        'days': WEEK_DAYS,
        'building': BUILDINGS,
        'results': True,
        'message': values['message']
    }
    return render(request, 'web_app/form.html', context)


def handle_post_request(request, form):
    # Get form values
    values = get_form_dictionary(form)
    if values['room_number'] and values['building']:
        return option_one(request, values)
    # TODO:
    elif True:
        return option_two(request, values)
    else:
        return HttpResponse('<h1>Error!</h1>')


def handle_get_request(request, message=None):
    render(request, 'web_app/popup.html')
    return render(request, 'web_app/form.html',
                  {
                      'buildings': BUILDINGS,
                      'days': WEEK_DAYS,
                      'message': message,
                      'show_popup': True
                  })


def index(request):
    print('HERE')
    # Handle post requests
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            return handle_post_request(request, form)
        else:
            error_message = '- There was an error in your form submission, Fill all required fields with valid data!'
            return handle_get_request(request, error_message)
    elif request.method == 'GET':
        return handle_get_request(request)
    # If requests received is not GET or POST (ie. PUT or DELETE, ect...) then redirect to the main page
    else:
        return HttpResponse('<h1>Error!</h1>')


# TRACKING
##############################################################################################################################################################


# tracking wants to accept more formats than default, here they are
INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%Y-%m',  # '2006-10'
    '%Y',  # '2006'
]


class DashboardForm(forms.Form):
    start = forms.DateTimeField(required=False, input_formats=INPUT_FORMATS)
    end = forms.DateTimeField(required=False, input_formats=INPUT_FORMATS)


@permission_required('tracking.visitor_log')
def dashboard(request):
    "Counts, aggregations and more!"

    end_time = now()
    start_time = end_time - timedelta(days=7)
    defaults = {'start': start_time, 'end': end_time}

    form = DashboardForm(data=request.GET or defaults)
    if form.is_valid():
        start_time = form.cleaned_data['start']
        end_time = form.cleaned_data['end']

    # determine when tracking began
    try:
        obj = Visitor.objects.order_by('start_time')[0]
        track_start_time = obj.start_time
    except (IndexError, Visitor.DoesNotExist):
        track_start_time = now()

    # If the start_date is before tracking began, warn about incomplete data
    warn_incomplete = (start_time < track_start_time)

    # queries take `date` objects (for now)
    user_stats = Visitor.objects.user_stats(start_time, end_time)
    visitor_stats = Visitor.objects.stats(start_time, end_time)
    if TRACK_PAGEVIEWS:
        pageview_stats = Pageview.objects.stats(start_time, end_time)
    else:
        pageview_stats = None

    context = {
        'form': form,
        'track_start_time': track_start_time,
        'warn_incomplete': warn_incomplete,
        'user_stats': user_stats,
        'visitor_stats': visitor_stats,
        'pageview_stats': pageview_stats,
    }
    return render(request, 'tracking/dashboard.html', context)


##############################################################################################################################################################


def feedback(request):
    # TODO: Build feedback page
    return render(request, 'web_app/feedback.html')


def csrf_failure(request, reason=""):
    return HttpResponse('<h1>Ouch you just hit an error! Maybe try stop playing around :D</h1>')

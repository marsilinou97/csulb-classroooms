# from sys import path
# path.insert(0, '../../utilities')
from django.shortcuts import render
from django.http import HttpResponse
from . import DAO
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from builtins import enumerate

connector = DAO.database_access_object()





def index(request):
    pass
    # context = {
    #     'classes': ''
    # }
    #
    # return render(request, 'web_app/index.html', buil)


def feedback(request):
    return render(request, 'web_app/feedback.html')


def test(request):
    # buildings = connector.get_buildings()
    # days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # values = {'buildings': buildings, 'days':days[:-2]}
    # return render(request, 'web_app/test.html', values)
    currentDT = datetime.now()
    finalTime = ['', '']
    days = {'Monday': 'M',
            'Tuesday': 'Tu',
            'Wednesday': 'W',
            'Thursday': 'Th',
            'Friday': 'F',
            'Saturday': 'St',
            'Sunday': 'Su'
            }
    week_days = {
        'Monday': 'M',
        'Tuesday': 'Tu',
        'Wednesday': 'W',
        'Thursday': 'Th',
        'Friday': 'F'
    }
    cursor = 'connection.cursor()'

    buildings = connector.get_buildings()
    if request.method == 'POST':
            start_time_filter = request.POST.get('start_time')
            end_time_filter = request.POST.get('end_time')
            building = request.POST.get('building')
            room = request.POST.get('room_number')
            day = request.POST.get('day')

            if not start_time_filter:
                start_time_filter = currentDT.strftime("%I:%M%p")
            if not end_time_filter:
                end_time_filter = (currentDT + timedelta(minutes=30)).strftime("%I:%M%p")
            if not day or len(day) not in range(1, 3):
                day = days[currentDT.strftime('%A')] if days[currentDT.strftime('%A')] not in ['St', 'Sn'] else 'M'
            finalTime = start_time_filter, end_time_filter
            results = connector.get_rooms(start_time_filter, end_time_filter, day, room, building)
            render(request, 'web_app/results_table.html', {'schedule': results})
            return render(request, 'web_app/test.html', {
                'schedule': results,
                'buildings': buildings,
                'resultsCount': len(results),
                'finalTime': finalTime,
                'days': week_days,
                'day': day,
                'building': building,
                'results': True})
    else:
        return render(request, 'web_app/test.html',
                      {
                          'buildings': buildings,
                          'days': week_days
                      })

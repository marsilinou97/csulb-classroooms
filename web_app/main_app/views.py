# from sys import path
# path.insert(0, '../../utilities')
from datetime import datetime, timedelta

from django.shortcuts import render

from . import DAO
from .forms import QueryForm

connector = DAO.database_access_object()


def index(request):
    pass


def feedback(request):
    return render(request, 'web_app/feedback.html')


global buildings
buildings = dict()


def test(request):
    global buildings
    finalTime = []
    currentDT = datetime.now()
    week_days = {'Monday': 'M', 'Tuesday': 'Tu', 'Wednesday': 'W', 'Thursday': 'Th', 'Friday': 'F'}
    if not buildings:
        print("We have to fetch buildings from db :/")
        buildings = connector.get_buildings()
    else:
        print("We have buildings stored yaaaay!")


    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            print(f"Form data: {form.cleaned_data.values()}")
            values = dict()
            values['start_time'] = form.cleaned_data['start_time']
            values['end_time'] = form.cleaned_data['end_time']
            values['day'] = form.cleaned_data['day']
            values['room_number'] = form.cleaned_data['room_number']
            values['building'] = form.cleaned_data['building']
            if not values['start_time']:
                values['start_time'] = currentDT.strftime("%I:%M%p")
            if not values['end_time']:
                values['end_time'] = (currentDT + timedelta(minutes=30)).strftime("%I:%M%p")
            if not values['day'] or len(values['day']) not in range(1, 3):
                day = week_days[currentDT.strftime('%A')] if week_days[currentDT.strftime('%A')] not in ['St','Su'] else 'M'
            finalTime = values['start_time'], values['end_time']
            for k,v in values.items():
                if not v:
                    values[k] = '%'
            results = connector.get_rooms(start_time=values['start_time'],
                                          end_time=values['end_time'],
                                          day=week_days[values['day']],
                                          room_number=values['room_number'],
                                          building=values['building']
                                          )
            render(request, 'web_app/results_table.html', {'schedule': results})

            return render(request, 'web_app/test.html', {
                'schedule': results,
                'buildings': buildings,
                'resultsCount': len(results),
                'finalTime': finalTime,
                'days': week_days,
                'day': day,
                'building': buildings,
                'results': True})
        else:
            print(f"Form data: {form.clean()}")
            return render(request, 'web_app/test.html',
                          {
                              'buildings': buildings,
                              'days': week_days,
                          })


    else:
        return render(request, 'web_app/test.html',
                      {
                          'buildings': buildings,
                          'days': week_days
                      })

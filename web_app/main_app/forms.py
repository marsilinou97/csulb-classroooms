from django import forms


class QueryForm(forms.Form):
    start_time = forms.CharField(max_length=5, required=True)
    end_time = forms.CharField(max_length=5, required=True)
    day = forms.CharField(max_length=10, required=True)
    room_number = forms.CharField(max_length=7, required=False)
    building = forms.CharField(max_length=7, required=True)

from django import forms
from .models import Booking
import datetime

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'date', 'time', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'time': forms.TimeInput(attrs={'type': 'time', 'min': '09:00', 'max': '19:00'}, format='%H:%M'),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time:
            if time < datetime.time(9, 0) or time > datetime.time(19, 0):
                raise forms.ValidationError("Выберите время с 09:00 до 19:00.")
        return time

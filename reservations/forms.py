from django import forms
from django.utils import timezone
from .models import Reservation
from django.core.exceptions import ValidationError


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('date', 'time', 'party_size')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'party_size': forms.NumberInput(attrs={'min': 1, 'max': 10, 'placeholder': 'Guests (1-10)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Signature Orlantech styling applied dynamically
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-4 bg-up-light/30 border border-up-secondary/10 rounded-xl focus:ring-2 focus:ring-up-primary focus:border-up-primary transition-all duration-300 outline-none font-medium text-up-secondary'
            })

    def clean_date(self):
        """Prevents booking in the past."""
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("We cannot travel back in time. Please select a future date.")
        return date

    def clean(self):
        """Cross-field validation (e.g., checking operating hours)."""
        cleaned_data = super().clean()
        time = cleaned_data.get('time')

        # Example: Business hours check (6 AM to 1:30 AM)
        if time:
            hour = time.hour
            # If time is between 2 AM and 5 AM, it's closed
            if 2 <= hour <= 5:
                raise ValidationError(
                    "Urban Palate is closed for deep cleaning during these hours. Please choose between 06:00 and 01:30.")

        return cleaned_data
from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    """
    Form for creating a new reservation, using fields available in the Reservation model.
    Only includes fields the user should manually set.
    """

    class Meta:
        model = Reservation
        # CRITICAL FIX: Only include fields present in the Reservation model
        fields = ('date', 'time', 'party_size')

        # Add widgets for better UX (Tailwind classes for styling and HTML5 type for inputs)
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-up-primary focus:border-up-primary',
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-up-primary focus:border-up-primary',
            }),
            'party_size': forms.NumberInput(attrs={
                'min': 1,
                'max': 10,
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-up-primary focus:border-up-primary',
                'placeholder': 'Number of Guests (1-10)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure all fields have the standard styling
        for _, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-up-primary focus:border-up-primary'
            })
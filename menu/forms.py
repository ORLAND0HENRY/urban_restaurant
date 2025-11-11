from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        label="Your Rating (1-5)",
        widget=forms.Select(attrs={'class': 'shadow-soft rounded-lg'})
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience with this dish...'}),
        label="Your Review/Comment"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rating',
            'comment',
            Submit('submit', 'Submit Review', css_class='bg-up-secondary text-up-light hover:bg-up-primary transition duration-200 mt-4 rounded-lg')
        )
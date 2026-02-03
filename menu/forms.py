from django import forms
from .models import Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'bg-neutral-900 border-white/10 text-amber-500 rounded-xl focus:ring-amber-500 focus:border-amber-500'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell us about the flavor profile...',
                'class': 'bg-neutral-900 border-white/10 text-white rounded-xl focus:ring-amber-500 focus:border-amber-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False  # Keep it minimalist and urban
        self.helper.layout = Layout(
            Field('rating', placeholder="Rate 1-5"),
            Field('comment'),
            Submit('submit', 'Post Review',
                   css_class='w-full py-3 bg-amber-500 text-black font-black uppercase rounded-xl hover:bg-amber-400 transition-all active:scale-95 shadow-lg shadow-amber-500/20')
        )

    def clean_comment(self):

        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError("Your review is a bit short. Tell us more about the dish!")
        return comment
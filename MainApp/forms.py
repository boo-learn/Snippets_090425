from django import forms
from MainApp.models import LANG_CHOICES, Snippet



class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["name", "lang", "code"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название сниппета'}),
            'lang': forms.Select(
                choices=LANG_CHOICES,
                attrs={'class': 'form-control'}
            ),
            'code': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Код сниппета'}),
        }

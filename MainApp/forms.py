from django import forms
from MainApp.models import LANG_CHOICES, Snippet



class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["name", "lang", "code", "public"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название сниппета'}),
            'lang': forms.Select(
                choices=LANG_CHOICES,
                attrs={'class': 'form-control'}
            ),
            'code': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Код сниппета'}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if len(name) < 5:
            raise forms.ValidationError("Name too short")
        return name

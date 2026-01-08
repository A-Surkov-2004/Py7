from django import forms

class NewPollForm(forms.Form):
    question_text = forms.CharField(
        label='Вопрос опроса',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    choices = forms.CharField(
        label='Варианты ответов',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Каждый вариант с новой строки'
        })
    )
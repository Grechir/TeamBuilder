from django import forms
from .models import UserResponse

class ResponseSearchForm(forms.Form):

    author = forms.ChoiceField(
        choices=[
            ('all', 'Все'),
            ('outgoing', 'Исходящие'),
            ('incoming', 'Входящие'),
        ],
        required=False,
        label='Отправитель'
    )

    status = forms.ChoiceField(
        choices=[('', 'Все')] + list(UserResponse.STATUS_CHOICES),
        required=False,
        label='Статус'
    )

    post_title = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Отклики',
        empty_label='Все посты'
    )

    def __init__(self, *args, **kwargs):
        user_posts = kwargs.pop('user_posts')
        super().__init__(*args, **kwargs)

        if user_posts:
            self.fields['post_title'].queryset = user_posts






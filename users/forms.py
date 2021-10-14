import re

from django.contrib.auth.forms import UserCreationForm

from users.models import User


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean(self):
        cleaned_data = super(CreationForm, self).clean()
        username = cleaned_data.get('username')
        print(username)
        if not re.match(r'[a-z_][0-9a-z_]*$', username):
            self.add_error('username',
                           'Допустимы только буквы латинского алфавита, '
                           'цифры и нижнее подчеркивание. Username не может '
                           'начинаться с цифры')
        return cleaned_data

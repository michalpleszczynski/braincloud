from django.forms import Form, CharField, Textarea, EmailField, TextInput
from django.contrib.auth.forms import UserCreationForm

from common.utils import utcnow
from .models import TextThought


class TextThoughtForm(Form):
    title = CharField(max_length = 120)
    content = CharField(max_length = 1000, widget = Textarea)
    tags = CharField(max_length = 320)

    def get_thought(self):
        if not self.is_valid():
            # throw exception?
            pass
        thought = TextThought(title = self.cleaned_data['title'], content = self.cleaned_data['content'])
        thought.tags = set(item.strip() for item in self.cleaned_data['tags'].split(","))
        thought.last_update = utcnow()
        return thought


class UserRegistrationForm(UserCreationForm):
    email = EmailField(widget=TextInput(attrs={'placeholder': 'email'}))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'password (again)'})


class SearchForm(Form):
    query = CharField(max_length = 120)
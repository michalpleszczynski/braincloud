import datetime

from django.forms import Form, CharField, Textarea, EmailField
from django.contrib.auth.forms import UserCreationForm

from .models import Thought

class ThoughtForm(Form):
    title = CharField(max_length = 120)
    content = CharField(max_length = 1000, widget = Textarea)
    tags = CharField(max_length = 320)

    def get_thought(self):
        if not self.is_valid():
            # throw exception?
            pass
        thought = Thought(title = self.cleaned_data['title'], content = self.cleaned_data['content'])
        thought.tags = [item.strip() for item in self.cleaned_data['tags'].split(",")]
        thought.last_update = datetime.datetime.now()
        return thought
    
class UserRegistrationForm(UserCreationForm):
    email = EmailField()
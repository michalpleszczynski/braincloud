from django.forms import Form, CharField, Textarea

class ThoughtForm(Form):
    title = CharField(max_length = 120)
    content = CharField(max_length = 1000, widget = Textarea)
    tags = CharField(max_length = 320)


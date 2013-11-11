import random
import datetime

from pymongo import MongoClient

CLEANUP = True
DB_NAME = 'braincloud'

AUTHORS = ['michau']

MIN_TITLE = 5
MAX_TITLE = 60

MIN_CONTENT = 10
MAX_CONTENT = 1000

MIN_TAG = 1
MAX_TAG = 10
MAX_TAG_SUM = 100

text = ''
tag_list = []


def generate(number=300):
    thoughts = []
    user_tags = {}
    print "Generating %d entries." % number
    for i in range(number):
        thought = {
            'author': random.choice(AUTHORS),
            'title': _get_random_text(random.randint(MIN_TITLE, MAX_TITLE)),
            'content': _get_random_text(random.randint(MIN_CONTENT, MAX_CONTENT)),
            'last_update': datetime.datetime.now(),
            'tags': _get_random_tags(random.randint(MIN_TAG, MAX_TAG)),
        }
        if thought['author'] not in user_tags:
            user_tags[thought['author']] = {}
        for tag in thought['tags']:
            if tag not in user_tags[thought['author']]:
                user_tags[thought['author']][tag] = 1
            else:
                user_tags[thought['author']][tag] += 1
        thoughts.append(thought)

    user_tags_ext = []
    for item in user_tags.iteritems():
        user_tag = {
            '_id': item[0],
            'tags': item[1]
        }
        user_tags_ext.append(user_tag)

    client = MongoClient()
    db = client[DB_NAME]
    if CLEANUP:
        print "Performing cleanup"
        db.thought.remove()
        db.user_tags.remove()
    print "Saving %d thoughts and %s and tag entries to db." % (len(thoughts), len(user_tags_ext))
    db.thought.insert(thoughts)
    db.user_tags.insert(user_tags_ext)
    client.close()


def _get_random_text(length=500):
    global text
    if len(text) == 0:
        with open('dict.txt') as data:
            text = data.read()
    if length >= len(text):
        return text
    s_index = random.randint(0, len(text) - length - 1)
    e_index = s_index + length
    return text[s_index:e_index]


def _get_random_tags(length=4):
    global tag_list
    if len(tag_list) == 0:
        with open('tag_dict.txt') as data:
            tag_list = data.readlines()
    if length >= len(tag_list):
        return tag_list
    result = []
    sum_len = 0
    for i in range(length):
        tag = random.choice(tag_list)
        sum_len += len(tag)
        result.append(tag.strip())
        if sum_len >= MAX_TAG_SUM:
            break
    return result

if __name__ == "__main__":
    generate()
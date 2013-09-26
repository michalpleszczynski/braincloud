from random import randint
from math import log

# def prepare_test_data(tags_number = 100, min_count = 0, max_count = 1000):
#     tags = {}
#     for i in range(tags_number):
#         tags['tag' + str(i)] = randint(min_count, max_count)
#     return tags
# 
# def get_data_from_file(filename = '../static/us_domains.txt'):
#     tags = {}
#     with open(filename,'r') as data:
#         for line in data:
#             domain, count = line.split(':')[0], int(line.split(':')[1])
#             tags[domain] = count
#     return tags

def calculate_sizes(tag_dict, threshold = 1, min_size = 1, max_size = 10):
    min_count, max_count = min(tag_dict.values()), max(tag_dict.values())
    min_count = threshold if threshold > min_count else min_count
    constant = log(max_count - min_count or 1)/(max_size - min_size)
    tag_size = {}
    for tag, count in tag_dict.iteritems():
        if count >= threshold:
            tag_size[tag] = min_size + log(count - min_count or 1)/constant
    return tag_size
    
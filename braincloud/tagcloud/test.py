from utils import *

tags = prepare_test_data()
#tags = get_data_from_file()
tags['tag1231'] = 500
tag_size = calculate_sizes(tags, 500)
for item in tag_size.iteritems():
	print item[0] + ' : ' + str(item[1])
print len(tag_size)


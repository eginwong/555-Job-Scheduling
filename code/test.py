import datetime
import csv
import heapq

start_date = "01-Apr-16"
date_1 = datetime.datetime.strptime(start_date, "%d-%b-%y")

end_date = date_1 + datetime.timedelta(days=3)

print str(date_1) + " and " + str(end_date)
print date_1.weekday()
print end_date.weekday()

heap = []

# add some values to the heap
for value in [20, 10, 30, 50, 40]:
    heapq.heappush(heap, value)

# pop them off, in order
print "First value is: " + str(heap[0])
while heap:
    print heapq.heappop(heap)

h = []
heapq.heappush(h, (5, 'write code'))
heapq.heappush(h, (7, 'release product'))
heapq.heappush(h, (1, 'write spec'))
heapq.heappush(h, (3, 'create tests'))
print h
#
# #check if date is before due date.
# print date_1 < end_date
#
# #if weekday = 0, Monday. if weekday >4, move day by 2
# print date_1.weekday()

#
# #To start off counter for csv read.
# start_num = 0
# dictJobs = {}
# powwowList = []
# #read in the csv.
# with open('input.csv', 'rb') as f:
#     reader = csv.reader(f)
#     for i, line in enumerate(reader):
# 	if(int(line[0]) != None and line[0] > 0):
#             assert type(line[0]) == int, "FUCK NOT INT"
# 	    powwowList.append(line)
#             start_num = line[0]
# 	    print start_num
#             print 'line[{}] = {}'.format(i, line)
#
# print("-----------------------------------------------------------------------------------------------------")
# print("-----------------------------------------------------------------------------------------------------")
# print("-----------------------------------------------------------------------------------------------------")
# print '[%s]' % ', '.join(map(str, powwowList))
# print ("Jobs" > 0)

import datetime
import csv

start_date = "01-Apr-16"
date_1 = datetime.datetime.strptime(start_date, "%d-%b-%y")

end_date = date_1 + datetime.timedelta(days=3)

print str(date_1) + " and " + str(end_date)
print date_1.weekday()
print end_date.weekday()
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

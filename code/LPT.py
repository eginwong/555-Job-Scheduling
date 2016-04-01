# need time, machine status
# do we need to convert days to time?
# http://stackoverflow.com/questions/6871016/adding-5-days-to-date-in-python
#
# Define job as array of job#, stage, release, end, lateness, actual data of stages.
#
# t=0 to start
# start_date;
#
# While jobs are in queue or in transit
# {
#
# Check date and add available jobs to queue
# 	What's released by date
# 	Check what's in transit
# Refresh machines (Complete any jobs that are there)
# 	If jobs are finished, calculate lateness
# 	Else: toss into transit queue with time it's finished
#
# for each job in queue, check if machine is free. If yes, assign job to machine queue.
# 	when assigning, store job#, t=expected end
#
# update time to next event (machine is free)
# update actual date as well.
# 	take difference in i
#   i is most important counter, date is only to indicate ending date + release date
#
# 	if (day is Friday){
# 		if i >= 7.5
# 			move one day over
# 	}
# 	(complicated part of sorting out times from finishing machines)
# }
#
# Finally, calculate total percentage of jobs that are late. If lateness exists, increment counter by 1, divide by length of array.

import datetime
import csv

#To start off counter for csv read.
start_num = 0
dictJobs = {}
powwowList = []
#read in the csv.
with open('input.csv', 'rb') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
	if(int(line[0]) != None and line[0] > 0):
            assert type(line[0]) == int, "FUCK NOT INT"
	    powwowList.append(line)
            start_num = line[0]
	    print start_num
            print 'line[{}] = {}'.format(i, line)

print("-----------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------")
print("-----------------------------------------------------------------------------------------------------")
print '[%s]' % ', '.join(map(str, powwowList))
print ("Jobs" > 0)


# start_date = "10/10/11"
# date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
#
# end_date = date_1 + datetime.timedelta(days=52)
#
# print str(date_1) + " and " + str(end_date)
#
# #check if date is before due date.
# print date_1 < end_date
#
# #if weekday = 0, Monday. if weekday >4, move day by 2
# print date_1.weekday()

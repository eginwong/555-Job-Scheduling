import datetime
import csv
import heapq

dictJobs = {}
dictMachines = {}
#read in the csv.
with open('input.csv', 'rb') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(line[0].isdigit() and line[0] > 0):
            key = int(line[0])
            machine = line[3]

            #Define job as array of job#, stage, release, end, lateness, actual data of stages.
            if key in dictJobs:
                dictJobs[key]["data"].append([line[3],line[4]])
            else:
                dictJobs[key] = {"stage": 1, "release": datetime.datetime.strptime(line[1], "%d-%b-%y"), "end": datetime.datetime.strptime(line[2], "%d-%b-%y"), "data": [[line[3], line[4]]]}

            #For machines:
            if machine not in dictMachines:
                dictMachines[machine] = None

print("################################    DICTIONARY    ################################")
print dictJobs
print "Total number of jobs in the dictionary: " + str(len(dictJobs))
print("################################    MACHINES    ################################")
print dictMachines
print "Total number of machines: " + str(len(dictMachines))

#qtransit: we will just use a list and store [job, machine, transitendtime]
qTransit = []
#qArrival: Stages of jobs that are released and available.
qArrival = []
#qService: Machines that are in use.
qService = []

# t is most important counter, date is only to indicate ending date + release date
t = 0

# Makes sense to start with the first job's release date. Hard code to 1 as there is no job #0.
current_date = dictJobs[1]['release']
current_hour = 0

# no "do-while" loop in python, using similar construct. http://stackoverflow.com/questions/1662161/is-there-a-do-until-in-python
while True:
    # Check date and add available jobs to queue - What's released by date
    for job in dictJobs:
        if job not in qArrival and dictJobs[job]["release"] <= current_date:
            #add to queue
            heapq.heappush(qArrival, (float(dictJobs[job]["data"][dictJobs[job]["stage"] - 1][1]), dictJobs[job]["data"][dictJobs[job]["stage"] - 1][0], job))
        #else: break ('cause we know nothing is shorter afterwards)
        else: break
    print "TEST RESULTS ********************************"
    print qArrival

    ###### Check what's in transit
    for job in qTransit:
        print job
        # if job.time > t : push onto regular queue
        # heapq.heappush(qArrival, this job)
    break

###### Refresh machines (Complete any jobs that are there)
# create an empty array for free machines (dictMachines)
# qService is defined as (i ending, machine, job)
# for each job in machine queue:
for machine in qService:
    # peek to see earliest time. If t > current_time, pop and do something.
    if t >= qService[0][0]:
        temp = heapq.heappop(qService)
        # If the job has further stages
        if dictJobs[temp[2]]["stage"] <= len(dictJobs[temp[2]]["data"]) + 1:
            dictJobs[temp[2]]["stage"] += 1
            # toss into transit queue with time it's finished
            heapq.heappush(qTransit, (t + 7.5, temp[2]))
        #   else: calculate lateness (job is finished)
        else:
        # Assume that lateness is by days and not by hours, rounded up.
        #     Do not need to factor in i because we don't care about the hour of the day
            difference = current_date - dictJobs[temp[2]]["end"]
            if difference > 0:
                dictJobs[temp[2]]["lateness"] = difference
            else:
                dictJobs[temp[2]]["lateness"] = 0
    # If earliest time is still in future, break.
    else:
        break
#
# for each job in qArrival, check if machine is free from dictMachines. If yes, assign job to machine queue. PRIORITY QUEUE FOR MACHINE QUEUE.
#  if job['data'][job['stage']-1][0] == empty machine
#    add to priority queue (job, + t=expected)
#
###### update time to next event (machine is free)
# pop from the machine priority queue and take the new t
#   take difference in t1 and t2

# update actual date as well.
# while difference between t1 and t2 > 0:
#   if current_date.weekday() < 4: #Mon-Thurs
#     if (current_hour + difference) > 15*0.8: #means that it's more than one day
#       current_hour = 0 #reset
#       current_date = datetime.timedelta(days=1)
#     else:
#       current_hours += difference
#   if current_date.weekday() == 4: #Fri
#     if (current_hour + difference) > 7.5*0.8: #means that it's more than one day
#       current_hour = 0 #reset
#       current_date = datetime.timedelta(days=3) #move to Monday
#     else:
#       current_hours += difference
#

    # While jobs are in queue or in transit
    if len(qArrival) == 0 and len (qTransit) == 0:
        print "broken"
        break

################################    RESULTS    ################################
max_lateness = 0
percentage_late = 0
# for job in dictJobs:
#     temp = dictJobs[job]['lateness']
#     if temp > max_lateness:
#         max_lateness = temp
#     if temp > 1:
#         percentage_late += 1
#     percentage_late = percentage_late / len(dictJobs)
# print "################################    RESULTS    ################################"
# print "The max lateness is: " + str(max_lateness) + "."
# print "The percentage late is: " + str(percentage_late) + "."

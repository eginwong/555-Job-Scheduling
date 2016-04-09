import datetime
import csv
import heapq

def printDate( current_date ):
    switcher = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
    }
    print "++++++++++++++++++++++++++++++++++++++++++++++++ It is currently " + switcher[current_date.weekday()] + " " + str(current_date) + " ++++++++++++++++++++++++++++++++++++++++++++++++"
    return None

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
                dictMachines[machine] = False

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
#qLeft: to signify jobs that have been completed.
qLeft = []

# t is most important counter, date is only to indicate ending date + release date
t = 0

# Makes sense to start with the first job's release date. Hard code to 1 as there is no job #0.
current_date = dictJobs[1]['release']
current_hour = 0

# no "do-while" loop in python, using similar construct. http://stackoverflow.com/questions/1662161/is-there-a-do-until-in-python
while True:
    # Check date and add available jobs to queue - What's released by date
    for job in dictJobs:
        tupleVal = (float(dictJobs[job]["data"][dictJobs[job]["stage"] - 1][1]), dictJobs[job]["data"][dictJobs[job]["stage"] - 1][0], job)
        tupleValServ = (float(dictJobs[job]["data"][dictJobs[job]["stage"] - 2][1]), dictJobs[job]["data"][dictJobs[job]["stage"] - 2][0], job)
        tupleValServ = (float(dictJobs[job]["data"][dictJobs[job]["stage"] - 2][1]), dictJobs[job]["data"][dictJobs[job]["stage"] - 2][0], job)
        if job not in qLeft and tupleVal not in qArrival and tupleValServ not in qService and tupleValOld not in qTransit and dictJobs[job]["release"] <= current_date:
            #add to queue
            heapq.heappush(qArrival, tupleVal)
        #else: break ('cause we know nothing is shorter afterwards)
        else: break

    ###### Check what's in transit
    while len(qTransit) > 0 :
        # if job.time > t : push onto regular queue
        if t >= qTransit[0][0]:
            job = heapq.heappop(qTransit)
            heapq.heappush(qArrival, (float(dictJobs[job[1]]["data"][dictJobs[job[1]]["stage"] - 1][1]), dictJobs[job[1]]["data"][dictJobs[job[1]]["stage"] - 1][0], job[1]))
        else:
            break

    ###### Refresh machines (Complete any jobs that are there)
    # create an empty array for free machines (dictMachines)
    # qService is defined as (i ending, machine, job)
    # for each job in machine queue:
    for machine in qService:
        # peek to see earliest time. If t > current_time, pop and do something.
        if t >= qService[0][0]:
            temp = heapq.heappop(qService)
            # release the machine.
            dictMachines[temp[2]] = False;
            # If the job has further stages
            if dictJobs[temp[1]]["stage"] < len(dictJobs[temp[1]]["data"]):
                dictJobs[temp[1]]["stage"] += 1
                # toss into transit queue with time it's finished
                heapq.heappush(qTransit, (t + 7.5, temp[1]))
            #   else: calculate lateness (job is finished)
            else:
                qLeft.append(temp[1])
                # Assume that lateness is by days and not by hours, rounded up.
                # Do not need to factor in i because we don't care about the hour of the day
                difference = (current_date - dictJobs[temp[1]]["end"]).days
                if difference > 0:
                    dictJobs[temp[1]]["lateness"] = difference
                else:
                    dictJobs[temp[1]]["lateness"] = 0
        # If earliest time is still in future, break.
        else:
            break

    print "****************** PREP RESULTS ********************************"
    print "qArrival contains: " + str(qArrival)
    print "qService contains: " + str(qService)
    print "qTransit contains: " + str(qTransit)
    print "qLeft contains: " + str(qLeft)

    # for each job in qArrival, check if machine is free from dictMachines. If yes, assign job to machine queue. PRIORITY QUEUE FOR MACHINE QUEUE.
    qHolding = [] # Temporary queue to hold popped off jobs.
    while len(qArrival) > 0:
        tempJob = heapq.heappop(qArrival)
        print "Currently looking at assigning: " + str(tempJob)
        # if machine is empty for that job
        if not dictMachines[tempJob[1]]:
            print "ASSIGNED: " + str(tempJob[2])
            # add to priority queue (job, + t=expected)
            heapq.heappush(qService, (t + tempJob[0], tempJob[2], tempJob[1]))
            # Set machine index to true.
            dictMachines[tempJob[1]] = True
        else:
            heapq.heappush(qHolding, tempJob)
    # When the process has finished, replace arrival with holding to restore any previously popped values.
    qArrival = qHolding
    print "############################ AFTER JOB ASSIGNMENT ##########################"
    print "qArrival is: ",
    print qArrival
    print "qService is: ",
    print qService

    ###### update time to next event (machine is free)
    # pop from the machine priority queue and take the new t.
    #~~~~~~~~~~~~~~~If there is no service left, advance the time to the next arrival.
    if len(qService) > 0:
        finishedService = qService[0]
        tNew = finishedService[0]
        print "The new time is: " + str(tNew)
        # take difference in t1 and t2
        tdelta = tNew - t

        # update actual date as well.
        # while difference between t1 and t2 > 0:
        while tdelta > 0:
            if current_date.weekday() < 4: #Mon-Thurs
                if (current_hour + tdelta) > 15*0.8: #means that it's more than one day
                    current_hour = 0 #reset
                    current_date += datetime.timedelta(days=1)
                    tdelta -= 15*0.8 - current_hour
                    printDate(current_date)
                else:
                    current_hour += tdelta
                    tdelta = 0
            if current_date.weekday() == 4: #Fri
                if (current_hour + tdelta) > 7.5*0.8: #means that it's more than one day
                    current_hour = 0 #reset
                    current_date += datetime.timedelta(days=3) #move to Monday
                    tdelta -= 7.5*0.8 - current_hour
                    printDate(current_date)
                else:
                    current_hour += tdelta
                    tdelta = 0
        t = tNew
    else:
        # Advance time to next arrival.
        if len(qLeft) != len(dictJobs):
            current_hour = 0 #reset
            if current_date.weekday() < 4: #Mon-Thurs
                current_date += datetime.timedelta(days=1)
            else:
                current_date += datetime.timedelta(days=3) #move to Monday
            printDate(current_date)

    # While jobs are in queue or in transit
    if len(qArrival) == 0 and len (qTransit) == 0 and len (qService) == 0 and len(qLeft) == len(dictJobs):
        print "loop complete"
        break

################################    RESULTS    ################################
max_lateness = 0
percentage_late = 0
for job in dictJobs:
    temp = dictJobs[job]["lateness"]
    if temp > max_lateness:
        max_lateness = temp
    if temp > 1:
        percentage_late += 1
    percentage_late = percentage_late / len(dictJobs)
# print "################################    RESULTS    ################################"
print "The max lateness is: " + str(max_lateness) + "."
print "The percentage late is: " + str(percentage_late) + "."

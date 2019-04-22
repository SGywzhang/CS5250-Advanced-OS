'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import copy
import math

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    schedule = []
    current_time = 0
    waiting_time = 0
    rr_list = copy.deepcopy(process_list)
    while rr_list:
        for process in rr_list[:]:
            if(current_time < process.arrive_time):
                if(rr_list[0].arrive_time>current_time):
                    current_time=process.arrive_time
                continue
            schedule.append((current_time, process.id))
            waiting_time = waiting_time + (current_time - process.arrive_time)
            if(process.burst_time > time_quantum):
                current_time = current_time + time_quantum
                process.burst_time = process.burst_time - time_quantum
                process.arrive_time=current_time
            else:
                current_time = current_time + process.burst_time
                rr_list.remove(process)
    average_waiting_time = waiting_time/float(len(process_list))
    print('Average waiting time = '+str(average_waiting_time))
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    schedule = []
    current_time = 0
    waiting_time = 0
    count = index = 0
    length = len(process_list)
    rem_bt = [p.burst_time for p in process_list]

    while count < length:
        candidate_burst = [t for t in rem_bt[:index + 1] if t]

        if not len(candidate_burst):
            index += 1
            continue

        srtf_index = rem_bt.index(min(candidate_burst))
        process = process_list[srtf_index]

        if current_time < process.arrive_time:
            current_time = process.arrive_time

        if not len(schedule) or schedule[-1][1] != process.id:
            schedule.append((current_time, process.id))

        run_time = rem_bt[srtf_index]

        if index < length - 1: 
            nxt = process_list[index + 1]
            run_time = min(run_time, nxt.arrive_time - current_time)

            if current_time >= nxt.arrive_time:
                index += 1

        current_time += run_time
        rem_bt[srtf_index] -= run_time

        if not rem_bt[srtf_index]:
            waiting_time += current_time - process.arrive_time - process.burst_time
            count += 1

    average_waiting_time = waiting_time / float(length)
    print('Average waiting time = '+str(average_waiting_time))
    return schedule, average_waiting_time
  
def SJF_scheduling(process_list, alpha):
    schedule = []
    predict_list = {}
    finished = {}
    current_time = 0
    waiting_time = 0

    for process in process_list:
        predict_list[process.id] = 5
        finished[process] = False
    
    for process in process_list:
        waiting_list = []
        for i in range(len(process_list)):
            if(current_time >= process_list[i].arrive_time and finished[process_list[i]] != True):
                waiting_list.append(process_list[i])

        if(len(waiting_list) == 0):
            current_time = process.arrive_time
            waiting_list.append(process)

        min_index = 0
        for queue_process in waiting_list:
            if(predict_list[waiting_list[min_index].id] > predict_list[queue_process.id]):
                min_index = waiting_list.index(queue_process)
        if(len(schedule) == 0 or schedule[len(schedule) - 1][1] != waiting_list[min_index].id):
            schedule.append((current_time, waiting_list[min_index].id))
        finished[waiting_list[min_index]] = True
        if(current_time >= waiting_list[min_index].arrive_time):
            waiting_time += current_time - waiting_list[min_index].arrive_time
        current_time += waiting_list[min_index].burst_time

        predict_list[waiting_list[min_index].id] = alpha * waiting_list[min_index].burst_time + (1-alpha)*predict_list[waiting_list[min_index].id]
        
        waiting_list.pop(min_index)
  
    average_waiting_time = waiting_time / float(len(process_list))
    print('Average waiting time = '+str(average_waiting_time))
    return schedule, average_waiting_time


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

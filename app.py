project.py
Who has access
A
System properties
Type
Text
Size
36 KB
Storage used
36 KB
Location
OS project
Owner
Aly Sabie
Modified
Apr 28, 2021 by Aly Sabie
Opened
1:03 PM by me
Created
Apr 29, 2021
No description
Viewers can download
from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import random
from tkinter import messagebox
def fcfs(p1, bt, at): # p for process ... bt for burst time ... at for arrival time

	index = []
	length = p1
	wait = 0
	counter=0
	for i in range(len(at)):
		at[i]=int(at[i])
		bt[i]=int(bt[i])
	p1 =[*range(1,p1+1,1)]	
	for i in range(len(p1)):
			p1[i] = "P" + str(p1[i])
	# Sorting the three lists on the same index
	zipped_lists = zip(at, p1, bt)
	sorted_pairs = sorted(zipped_lists)
	tuples = zip(*sorted_pairs)
	at, p1, bt = [ list(tuple) for tuple in  tuples]

	
	start_sequence = []
	start_sequence.append(at[0])
	start_sequence.append(start_sequence[0] + bt[0])
	
	for i in range(1, length):
		if(start_sequence[i] >= at[i]):
			start_sequence.append(start_sequence[i] + bt[i])
		else:
			#print()
			index.append([at[i], i +1])
			start_sequence.append(at[i] + bt[i])
			p1.insert(i+counter, "P0")
			counter+=1
	loop = len(index)
	for j in reversed(range(0, loop)):
		start_sequence.insert(index[j][1], index[j][0])
		#print(j)

	#print(range(loop, 0))

	#print(p1)
	global p
	p=p1
	#print(start_sequence)
	global avg_wait
	return start_sequence
class priority:

	def processData(no_of_processes,list_arrival_time, list_burst_time, Priority_list):
		global avg_wait
		process_data = []
		process_id =[*range(1,no_of_processes+1,1)]
		#print(process_id)
		for i in range(len(list_arrival_time)):
			list_arrival_time[i]=int(list_arrival_time[i])
			list_burst_time[i]=int(list_burst_time[i])
			Priority_list[i]=int(Priority_list[i])
		for i in range(no_of_processes):
			temporary = []
			arrival_time = list_arrival_time[i]
			burst_time = list_burst_time[i]
			Priority=Priority_list[i]
			temporary.extend([process_id[i], arrival_time, burst_time, 0, burst_time,Priority])
			'''
			'0' is the state of the process. 0 means not executed and 1 means execution complete
			'''
			process_data.append(temporary)
		return priority.schedulingProcess(process_data)

	def schedulingProcess(process_data):
		sequence_of_process=[]
		start_time = []
		exit_time = []
		s_time = 0
		time_intervals = []
		process_data.sort(key=lambda x: x[1])
		for i in range(len(process_data)):
			for j in range(len(process_data)):
				if (process_data[i][1]==process_data[j][1]):
					if(process_data[j][5]-process_data[j][1]>process_data[i][5]-process_data[i][1]):
						process_data[i],process_data[j]=process_data[j],process_data[i]
		'''
		Sort processes according to the Arrival Time
		'''
		#print(process_data)
		if process_data[0][1]!=0:
			time_intervals.append(0)
			time_intervals.append(process_data[0][1])
			sequence_of_process.insert(0,"CPU FREE")
		else:
			time_intervals.append(0)
		for i in range(len(process_data)):
			ready_queue = []
			temp = []
			normal_queue = []

			for j in range(len(process_data)):
				if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
					temp.extend([process_data[j][0], process_data[j][1], process_data[j][2],process_data[j][5]])
					ready_queue.append(temp)
					temp = []
				elif process_data[j][3] == 0:
					temp.extend([process_data[j][0], process_data[j][1], process_data[j][2],process_data[j][5],process_data[j][5]-process_data[j][1]])
					normal_queue.append(temp)
					#print("qw",normal_queue)
					temp = []

			if len(ready_queue) != 0:
				ready_queue.sort(key=lambda x: x[3])
				'''
				Sort the processes according to the Burst Time
				'''
				#print(ready_queue)
				start_time.append(s_time)
				s_time = s_time + ready_queue[0][2]
				e_time = s_time
				exit_time.append(e_time)
				for k in range(len(process_data)):
					if process_data[k][0] == ready_queue[0][0]:
						break
				process_data[k][3] = 1
				process_data[k].append(e_time)
				time_intervals.append(time_intervals[-1]+ready_queue[0][2])
				sequence_of_process.append(ready_queue[0][0])
			elif len(ready_queue) == 0:
				normal_queue.sort(key=lambda x: x[1])
				for i in range(len(process_data)):
					if (normal_queue[0][1]==normal_queue[i][1]):
						if(normal_queue[0][4]>normal_queue[i][4]):
							normal_queue[i],normal_queue[0]=normal_queue[0],normal_queue[i]
				if s_time < normal_queue[0][1]:
					s_time = normal_queue[0][1]
				start_time.append(s_time)
				s_time = s_time + normal_queue[0][2]
				e_time = s_time
				exit_time.append(e_time)
				for k in range(len(process_data)):
					if process_data[k][0] == normal_queue[0][0]:
						break
				process_data[k][3] = 1
				process_data[k].append(e_time)
				time_intervals.append(time_intervals[-1]+process_data[-1][2])
				sequence_of_process.append(normal_queue[k][0])
				#print(k)
		time_intervals.append(process_data[sequence_of_process[-1]-1][6])
		t_time = priority.calculateTurnaroundTime(process_data)
		global avg_wait
		avg_wait = priority.calculateWaitingTime(process_data)
		time_intervals.pop(-1)
		#print(time_intervals)
		priority.printData(process_data, t_time, avg_wait)
		for i in range(len(sequence_of_process)):
			if sequence_of_process[i]!="CPU FREE":
				sequence_of_process[i] = "P" + str(sequence_of_process[i])
		global p
		p=sequence_of_process
		return time_intervals

	def calculateTurnaroundTime(process_data):
		total_turnaround_time = 0
		for i in range(len(process_data)):
			turnaround_time = process_data[i][6] - process_data[i][1]
			'''
			turnaround_time = completion_time - arrival_time
			'''
			total_turnaround_time = total_turnaround_time + turnaround_time
			process_data[i].append(turnaround_time)
		average_turnaround_time = total_turnaround_time / len(process_data)
		'''
		average_turnaround_time = total_turnaround_time / no_of_processes
		'''
		return average_turnaround_time


	def calculateWaitingTime(process_data):
		total_waiting_time = 0
		for i in range(len(process_data)):
			waiting_time = process_data[i][7] - process_data[i][2]
			'''
			waiting_time = turnaround_time - burst_time
			'''
			total_waiting_time = total_waiting_time + waiting_time
			process_data[i].append(waiting_time)
		average_waiting_time = total_waiting_time / len(process_data)
		'''
		average_waiting_time = total_waiting_time / no_of_processes
		'''
		return average_waiting_time


	def printData(process_data, average_turnaround_time, average_waiting_time):
		process_data.sort(key=lambda x: x[0])
		'''
		Sort processes according to the Process ID
		'''
		#print("Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time  Waiting_Time")

		#for i in range(len(process_data)):
			#for j in range(len(process_data[i])):

				#print(process_data[i][j], end="				")
			#print()

		#print(f'Average Turnaround Time: {average_turnaround_time}')

		#print(f'Average Waiting Time: {average_waiting_time}')


#if __name__ == "__main__":
 #   no_of_processes = int(input("Enter number of processes: "))
  #  sjf = SJF1()

class Prepriority:

	def processData(no_of_processes,list_arrival_time, list_burst_time,Priority_list):
		global avg_wait
		process_data = []
		for i in range(len(list_arrival_time)):
			list_arrival_time[i]=int(list_arrival_time[i])
			list_burst_time[i]=int(list_burst_time[i])
			Priority_list[i]=int(Priority_list[i])
		for i in range(no_of_processes):
			temporary = []
			process_id =[1,2,3,4]
			arrival_time = list_arrival_time[i]
			burst_time = list_burst_time[i]
			Priority=Priority_list[i]
			temporary.extend([process_id[i], arrival_time, burst_time, 0, burst_time,Priority])
			'''
			'0' is the state of the process. 0 means not executed and 1 means execution complete
			'''
			process_data.append(temporary)
		return Prepriority.schedulingProcess(process_data)

	def schedulingProcess(process_data):
		start_time = []
		exit_time = []
		s_time = 0
		sequence_of_process = []
		sequence_of_process1 = []
		time_intervals = []
		temp1=15
		counter=1
		process_data.sort(key=lambda x: x[1])
		'''
		Sort processes according to the Arrival Time
		'''
		while 1:
			ready_queue = []
			normal_queue = []
			temp = []
			for i in range(len(process_data)):
				if process_data[i][1] <= s_time and process_data[i][3] == 0:
					temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4],process_data[i][5]])
					ready_queue.append(temp)

					#print(ready_queue)
					temp = []
				elif process_data[i][3] == 0:
					temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4],process_data[i][5]])
					normal_queue.append(temp)
					#print("1",normal_queue)
					temp = []
			if len(ready_queue) == 0 and len(normal_queue) == 0:
				break
			if len(ready_queue) != 0:
				ready_queue.sort(key=lambda x: x[4])
				'''
				Sort processes according to priority
				'''
				start_time.append(s_time)
				s_time = s_time + 1
				e_time = s_time
				exit_time.append(e_time)
				sequence_of_process1.append(ready_queue[0][0])
				if(len(sequence_of_process)==0):
					sequence_of_process.append(ready_queue[0][0])
		 
				if(sequence_of_process[-1]!=ready_queue[0][0]):
					sequence_of_process.append(ready_queue[0][0])
				
				for k in range(len(process_data)):
					if process_data[k][0] == ready_queue[0][0]:
						break
				process_data[k][2] = process_data[k][2] - 1
				if process_data[k][2] == 0:        #If Burst Time of a process is 0, it means the process is completed
					process_data[k][3] = 1
					process_data[k].append(e_time)
			if len(ready_queue) == 0:
				if s_time < normal_queue[0][1]:
					s_time = normal_queue[0][1]
				start_time.append(s_time)
				s_time = s_time + 1
				e_time = s_time
				exit_time.append(e_time)
				sequence_of_process1.append(normal_queue[0][0])
				if(len(sequence_of_process)==0):
					sequence_of_process.append(normal_queue[0][0])
				if(sequence_of_process[-1]!=normal_queue[0][0]):
					sequence_of_process.append(normal_queue[0][0])
				for k in range(len(process_data)):
					if process_data[k][0] == normal_queue[0][0]:
						break
				process_data[k][2] = process_data[k][2] - 1
				if process_data[k][2] == 0:        #If Burst Time of a process is 0, it means the process is completed
					process_data[k][3] = 1
					process_data[k].append(e_time)

		for i in range(len(sequence_of_process)):
			sequence_of_process[i] = "P" + str(sequence_of_process[i]) 
		if process_data[0][1] !=0 and len(time_intervals)==0:
			time_intervals.append(0)
			time_intervals.append(process_data[0][1])
			sequence_of_process.insert(0,"CPU FREE")
		if process_data[0][1] ==0:
			time_intervals.append(0)
		t_time = Prepriority.calculateTurnaroundTime(process_data)
		global avg_wait
		avg_wait = Prepriority.calculateWaitingTime(process_data)
		Prepriority.printData(process_data, t_time, avg_wait, sequence_of_process)
		for i in range(len(sequence_of_process1)-1):
			if sequence_of_process1[i+1]==sequence_of_process1[i]:
				counter+=1
			else:
				time_intervals.append(time_intervals[-1]+counter)
				counter=1
		time_intervals.append(process_data[sequence_of_process1[-1]-1][6])
		#print(process_data)
		#print(time_intervals)
		#print(sequence_of_process1)
		global p
		p=sequence_of_process
		return time_intervals
	def calculateTurnaroundTime(process_data):
		total_turnaround_time = 0
		for i in range(len(process_data)):
			turnaround_time = process_data[i][6] - process_data[i][1]
			'''
			turnaround_time = completion_time - arrival_time
			'''
			total_turnaround_time = total_turnaround_time + turnaround_time
			process_data[i].append(turnaround_time)
		average_turnaround_time = total_turnaround_time / len(process_data)
		'''
		average_turnaround_time = total_turnaround_time / no_of_processes
		'''
		return average_turnaround_time

	def calculateWaitingTime(process_data):
		total_waiting_time = 0
		for i in range(len(process_data)):
			waiting_time = process_data[i][7] - process_data[i][4]
			'''
			waiting_time = turnaround_time - burst_time
			'''
			total_waiting_time = total_waiting_time + waiting_time
			process_data[i].append(waiting_time)
		average_waiting_time = total_waiting_time / len(process_data)
		'''
		average_waiting_time = total_waiting_time / no_of_processes
		'''
		return average_waiting_time

	def printData(process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
		process_data.sort(key=lambda x: x[0])
		'''
		Sort processes according to the Process ID
		'''
		#print("Process_ID  Arrival_Time  Rem_Burst_Time      Completed  Orig_Burst_Time Completion_Time  Turnaround_Time  Waiting_Time")
		#for i in range(len(process_data)):
			#for j in range(len(process_data[i])):
				#print(process_data[i][j], end="\t\t\t\t")
			#print()
		#print(f'Average Turnaround Time: {average_turnaround_time}')
		#print(f'Average Waiting Time: {average_waiting_time}')
		#print(f'Sequence of Process: {sequence_of_process}')

#if __name__ == "__main__":
   # no_of_processes = int(input("Enter number of processes: "))
   # sjf = SJF()
   # sjf.processData(no_of_processes)
class SJF1:
##non preemptive
	def processData(no_of_processes,list_arrival_time, list_burst_time):
		global avg_wait
		process_data = []
		process_id =[*range(1,no_of_processes+1,1)]
		#print(process_id)
		for i in range(len(list_arrival_time)):
			list_arrival_time[i]=int(list_arrival_time[i])
			list_burst_time[i]=int(list_burst_time[i])
		for i in range(no_of_processes):
			temporary = []
			arrival_time = list_arrival_time[i]
			burst_time = list_burst_time[i]
			temporary.extend([process_id[i], arrival_time, burst_time, 0, burst_time])
			'''
			'0' is the state of the process. 0 means not executed and 1 means execution complete
			'''
			process_data.append(temporary)
		return SJF1.schedulingProcess(process_data)

	def schedulingProcess(process_data):
		sequence_of_process=[]
		start_time = []
		exit_time = []
		s_time = 0
		time_intervals = []
		process_data.sort(key=lambda x: x[1])
		for i in range(len(process_data)):
			for j in range(len(process_data)):
				if (process_data[i][1]==process_data[j][1]):
					if(process_data[j][4]>process_data[i][4]):
						process_data[i],process_data[j]=process_data[j],process_data[i]
		'''
		Sort processes according to the Arrival Time
		'''
		#print(process_data)
		if process_data[0][1]!=0:
			time_intervals.append(0)
			time_intervals.append(process_data[0][1])
			sequence_of_process.insert(0,"CPU FREE")
		else:
			time_intervals.append(0)
		for i in range(len(process_data)):
			ready_queue = []
			temp = []
			normal_queue = []

			for j in range(len(process_data)):
				if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
					temp.extend([process_data[j][0], process_data[j][1], process_data[j][2],process_data[j][4]])
					ready_queue.append(temp)
					temp = []
				elif process_data[j][3] == 0:
					temp.extend([process_data[j][0], process_data[j][1], process_data[j][2],process_data[j][4]])
					normal_queue.append(temp)
					print("qw",normal_queue)
					temp = []

			if len(ready_queue) != 0:
				ready_queue.sort(key=lambda x: x[2])
				'''
				Sort the processes according to the Burst Time
				'''
				#print(ready_queue)
				start_time.append(s_time)
				s_time = s_time + ready_queue[0][2]
				e_time = s_time
				exit_time.append(e_time)
				for k in range(len(process_data)):
					if process_data[k][0] == ready_queue[0][0]:
						break
				process_data[k][3] = 1
				process_data[k].append(e_time)
				time_intervals.append(time_intervals[-1]+ready_queue[0][2])
				sequence_of_process.append(ready_queue[0][0])
			elif len(ready_queue) == 0:
				normal_queue.sort(key=lambda x: x[1])
				for i in range(len(process_data)):
					if (normal_queue[0][1]==normal_queue[i][1]):
						if(normal_queue[0][2]>normal_queue[i][2]):
							normal_queue[i],normal_queue[0]=normal_queue[0],normal_queue[i]
				if s_time < normal_queue[0][1]:
					s_time = normal_queue[0][1]
				start_time.append(s_time)
				s_time = s_time + normal_queue[0][2]
				e_time = s_time
				exit_time.append(e_time)
				for k in range(len(process_data)):
					if process_data[k][0] == normal_queue[0][0]:
						break
				process_data[k][3] = 1
				process_data[k].append(e_time)
				time_intervals.append(time_intervals[-1]+process_data[-1][2])
				sequence_of_process.append(normal_queue[k][0])
				print(k)
		time_intervals.append(process_data[sequence_of_process[-1]-1][5])
		t_time = SJF1.calculateTurnaroundTime(process_data)
		global avg_wait
		avg_wait = SJF1.calculateWaitingTime(process_data)
		time_intervals.pop(-1)
		print(time_intervals)
		SJF1.printData(process_data, t_time, avg_wait)
		for i in range(len(sequence_of_process)):
			if sequence_of_process[i]!="CPU FREE":
				sequence_of_process[i] = "P" + str(sequence_of_process[i])
		global p
		p=sequence_of_process
		return time_intervals

	def calculateTurnaroundTime(process_data):
		total_turnaround_time = 0
		for i in range(len(process_data)):
			turnaround_time = process_data[i][5] - process_data[i][1]
			'''
			turnaround_time = completion_time - arrival_time
			'''
			total_turnaround_time = total_turnaround_time + turnaround_time
			process_data[i].append(turnaround_time)
		average_turnaround_time = total_turnaround_time / len(process_data)
		'''
		average_turnaround_time = total_turnaround_time / no_of_processes
		'''
		return average_turnaround_time


	def calculateWaitingTime(process_data):
		total_waiting_time = 0
		for i in range(len(process_data)):
			waiting_time = process_data[i][6] - process_data[i][2]
			'''
			waiting_time = turnaround_time - burst_time
			'''
			total_waiting_time = total_waiting_time + waiting_time
			process_data[i].append(waiting_time)
		average_waiting_time = total_waiting_time / len(process_data)
		'''
		average_waiting_time = total_waiting_time / no_of_processes
		'''
		return average_waiting_time


	def printData(process_data, average_turnaround_time, average_waiting_time):
		process_data.sort(key=lambda x: x[0])
		'''
		Sort processes according to the Process ID
		'''
		print("Process_ID  Arrival_Time  Burst_Time      Completed  Completion_Time  Turnaround_Time  Waiting_Time")

		for i in range(len(process_data)):
			for j in range(len(process_data[i])):

				print(process_data[i][j], end="				")
			print()

		print(f'Average Turnaround Time: {average_turnaround_time}')

		print(f'Average Waiting Time: {average_waiting_time}')


#if __name__ == "__main__":
 #   no_of_processes = int(input("Enter number of processes: "))
  #  sjf = SJF1()

class SJF:

	def processData(no_of_processes,list_arrival_time, list_burst_time):
		global avg_wait
		process_data = []
		for i in range(len(list_arrival_time)):
			list_arrival_time[i]=int(list_arrival_time[i])
			list_burst_time[i]=int(list_burst_time[i])
		for i in range(no_of_processes):
			temporary = []
			process_id =[1,2,3,4]
			arrival_time = list_arrival_time[i]
			burst_time = list_burst_time[i]
			temporary.extend([process_id[i], arrival_time, burst_time, 0, burst_time])
			'''
			'0' is the state of the process. 0 means not executed and 1 means execution complete
			'''
			process_data.append(temporary)
		return SJF.schedulingProcess(process_data)

	def schedulingProcess(process_data):
		start_time = []
		exit_time = []
		s_time = 0
		sequence_of_process = []
		sequence_of_process1 = []
		time_intervals = []
		temp1=15
		counter=1
		process_data.sort(key=lambda x: x[1])
		'''
		Sort processes according to the Arrival Time
		'''
		while 1:
			ready_queue = []
			normal_queue = []
			temp = []
			for i in range(len(process_data)):
				if process_data[i][1] <= s_time and process_data[i][3] == 0:
					temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
					ready_queue.append(temp)

					#print(ready_queue)
					temp = []
				elif process_data[i][3] == 0:
					temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
					normal_queue.append(temp)
					#print("1",normal_queue)
					temp = []
			if len(ready_queue) == 0 and len(normal_queue) == 0:
				break
			if len(ready_queue) != 0:
				ready_queue.sort(key=lambda x: x[2])
				'''
				Sort processes according to Burst Time
				'''
				start_time.append(s_time)
				s_time = s_time + 1
				e_time = s_time
				exit_time.append(e_time)
				sequence_of_process1.append(ready_queue[0][0])
				if(len(sequence_of_process)==0):
					sequence_of_process.append(ready_queue[0][0])
		 
				if(sequence_of_process[-1]!=ready_queue[0][0]):
					sequence_of_process.append(ready_queue[0][0])
				
				for k in range(len(process_data)):
					if process_data[k][0] == ready_queue[0][0]:
						break
				process_data[k][2] = process_data[k][2] - 1
				if process_data[k][2] == 0:        #If Burst Time of a process is 0, it means the process is completed
					process_data[k][3] = 1
					process_data[k].append(e_time)
			if len(ready_queue) == 0:
				if s_time < normal_queue[0][1]:
					s_time = normal_queue[0][1]
				start_time.append(s_time)
				s_time = s_time + 1
				e_time = s_time
				exit_time.append(e_time)
				sequence_of_process1.append(normal_queue[0][0])
				if(len(sequence_of_process)==0):
					sequence_of_process.append(normal_queue[0][0])
				if(sequence_of_process[-1]!=normal_queue[0][0]):
					sequence_of_process.append(normal_queue[0][0])
				for k in range(len(process_data)):
					if process_data[k][0] == normal_queue[0][0]:
						break
				process_data[k][2] = process_data[k][2] - 1
				if process_data[k][2] == 0:        #If Burst Time of a process is 0, it means the process is completed
					process_data[k][3] = 1
					process_data[k].append(e_time)

		for i in range(len(sequence_of_process)):
			sequence_of_process[i] = "P" + str(sequence_of_process[i]) 
		if process_data[0][1] !=0 and len(time_intervals)==0:
			time_intervals.append(0)
			time_intervals.append(process_data[0][1])
			sequence_of_process.insert(0,"CPU FREE")
		if process_data[0][1] ==0:
			time_intervals.append(0)
		t_time = SJF.calculateTurnaroundTime(process_data)
		global avg_wait
		avg_wait = SJF.calculateWaitingTime(process_data)
		SJF.printData(process_data, t_time, avg_wait, sequence_of_process)
		for i in range(len(sequence_of_process1)-1):
			if sequence_of_process1[i+1]==sequence_of_process1[i]:
				counter+=1
			else:
				time_intervals.append(time_intervals[-1]+counter)
				counter=1
		time_intervals.append(process_data[sequence_of_process1[-1]-1][5])
		#print(process_data)
		#print(time_intervals)
		#print(sequence_of_process1)
		global p
		p=sequence_of_process
		return time_intervals
	def calculateTurnaroundTime(process_data):
		total_turnaround_time = 0
		for i in range(len(process_data)):
			turnaround_time = process_data[i][5] - process_data[i][1]
			'''
			turnaround_time = completion_time - arrival_time
			'''
			total_turnaround_time = total_turnaround_time + turnaround_time
			process_data[i].append(turnaround_time)
		average_turnaround_time = total_turnaround_time / len(process_data)
		'''
		average_turnaround_time = total_turnaround_time / no_of_processes
		'''
		return average_turnaround_time

	def calculateWaitingTime(process_data):
		total_waiting_time = 0
		for i in range(len(process_data)):
			waiting_time = process_data[i][6] - process_data[i][4]
			'''
			waiting_time = turnaround_time - burst_time
			'''
			total_waiting_time = total_waiting_time + waiting_time
			process_data[i].append(waiting_time)
		average_waiting_time = total_waiting_time / len(process_data)
		'''
		average_waiting_time = total_waiting_time / no_of_processes
		'''
		return average_waiting_time

	def printData(process_data, average_turnaround_time, average_waiting_time, sequence_of_process):
		process_data.sort(key=lambda x: x[0])
		'''
		Sort processes according to the Process ID
		'''
		#print("Process_ID  Arrival_Time  Rem_Burst_Time      Completed  Orig_Burst_Time Completion_Time  Turnaround_Time  Waiting_Time")
		#for i in range(len(process_data)):
			#for j in range(len(process_data[i])):
				#print(process_data[i][j], end="\t\t\t\t")
			#print()
		#print(f'Average Turnaround Time: {average_turnaround_time}')
		#print(f'Average Waiting Time: {average_waiting_time}')
		#print(f'Sequence of Process: {sequence_of_process}')

#if __name__ == "__main__":
   # no_of_processes = int(input("Enter number of processes: "))
   # sjf = SJF()
   # sjf.processData(no_of_processes)

def RR(number_of_processes, list_arrival_time, list_burst_time, q):

	#for j in range(number_of_processes)

	t = 0  # time
	list1 = []  # Output list contains the names of the processes
	list2 = []  # list contains the duration of each processes in list 1
	flag = 0  # When this flag=1, it means that all processes have been executed and the while loop terminates
	flag2 = 0  # When this flag=0, it means that some proccesses have not arrived yet so we will increment t till reaching the arrival time of the coming process
	wt = []  # waiting time array contains waiting time for each process

	for j in range(number_of_processes):
		list_arrival_time[j] = int(list_arrival_time[j])
		list_burst_time[j] = int(list_burst_time[j])


	list_burst_time_copy = []
	for i in range(len(list_burst_time)):
		list_burst_time_copy.append(list_burst_time[i])
	while flag == 0:
		flag2 = 0
		for i in range(number_of_processes):
			# This if will be executed once only in case all the processes do not arrive at time=0
			if int(t) < int(min(list_arrival_time)):
				t += min(list_arrival_time)
				list1.append(0)
				list2.append(min(list_arrival_time))
				flag2 = 1
			if list_arrival_time[i] <= t:
				if list_burst_time[i] >= q:
					list1.append(i + 1)
					list2.append(q)
					t += q
					list_burst_time[i] -= q
					flag2 = 1
					if list_burst_time[i] == 0:
						wt.append(t - list_arrival_time[i] - list_burst_time_copy[i])
				elif list_burst_time[i] < q and list_burst_time[i] != 0:
					list1.append(i + 1)
					list2.append(list_burst_time[i])
					t += list_burst_time[i]
					list_burst_time[i] = 0
					flag2 = 1
					wt.append(t - list_arrival_time[i] - list_burst_time_copy[i])
		if flag2 == 0:
			count = 0
			flag3 = 0  # if flag3=1, it indicates that t has been incremented a number of times=count until reaching the arrival time of the coming process
			while True:
				count += 1

				t += 1
				for l in range(number_of_processes):
					if list_arrival_time[l] == t:
						flag3 = 1
						break
				if flag3 == 1:
					list1.append(0)
					list2.append(count)
					break

		for k in range(number_of_processes):
			if list_burst_time[k] != 0:
				flag = 1
		if flag == 0:
			break
		flag = 0

	list3 = []  # Output list containing the start time of each process and the last element in it is the end time of the last process
	list3.append(0)
	for i in range(len(list2)):
		list3.append(list2[i] + list3[i])

	for i in range(len(list1)):
		list1[i] = "P" + str(list1[i]) 

	global p
	p = list1

	# calc avg waiting time from wt list
	global avg_wait
	for i in range(len(wt)):
		avg_wait += wt[i]
	avg_wait=avg_wait/number_of_processes

	return list3



#  The drawing function
def plot(starter, name):

	start = list(map(int, starter))  # converting each element of the list to an int
	#start.append(7)###################################################

	plt.figure(figsize=(10,2.5))
	font_p = {'family': 'serif',
			'color':  'white',
			'weight': 'bold',
			'size': 16,
			}

	print(start)
	length = len(starter) - 1 #len(start) - 1 
	x = []
	#print(range(length))
	for i in range(length):
		#random colour generation
		r = random.random()
		b = random.random()
		g = random.random()

		duration = start[i + 1] - start[i]
		
		x = [(start[i], duration)]
		avg = duration / 2
		place = avg + start[i]
		
		plt.broken_barh(x, (2,2), color=(r, g, b))
		plt.text(place - 0.17 , 2.9, name[i], fontdict=font_p)


	plt.show()


# Runned by the exit button to terminate the program
def exit():
	root.quit()

# Generators the process names in order     P1, P2, P3, ....
def id_generator(p, n):
	for i in range(1, n + 1):
		p.append("P" + str(i))

# Check whether the entered input is a number or not
def num_check():
	try:
		global n
		n = int(entry.get())
		return 0
	except ValueError:
		messagebox.showwarning("Invalid Input","Your input should be a number")
		return 1

def read(b, a, c):
	try:
		int(b)
		int(a)
		int(c)
		if(int(c)<1 or int(c)>5):
			c='s'
		int(c)
		bt.append(b)
		at.append(a)
		pr.append(c)
		global count
		count = count + 1
		sec_input()

	except ValueError:
		messagebox.showwarning("Invalid Input","Your input should be a number")
	
	

def finish(b, a, c):
	bt.append(b)
	at.append(a)
	pr.append(c)
	if (alg.get() == "Round Robin"):
		global quantumm
		quantumm = int(c)
		r = RR(n, at, bt, quantumm)                        ########################################################################
		#print(p)
		#print(r)
		#print(avg_wait)
		l4 = Label(root, text = avg_wait, padx = 3,  fg = "blue", font = "Veranda 14 italic bold" , bg="white")
		l4.grid(row=3, column=4)
		plot(r, p)       
	if (alg.get()=="FCFS"):
		r=fcfs(n,bt,at)
		l4 = Label(root, text = avg_wait, padx = 3,  fg = "blue", font = "Veranda 14 italic bold" , bg="white")
		l4.grid(row=3, column=4)
		#r=at
		#p=['p1','p2','p3']
		plot(r, p)
	if (alg.get() == "preemtive SJF"):
		r=SJF.processData(n,at,bt)
		#print(r)
		#print(p)
		l4 = Label(root, text = avg_wait, padx = 3,  fg = "blue", font = "Veranda 14 italic bold" , bg="white")
		l4.grid(row=3, column=4)
		plot(r, p)       
	if (alg.get()=="non_preemtive SJF"):
		r=SJF1.processData(n,at,bt)
		#print(r)
		#print(p)
		l4 = Label(root, text = avg_wait, padx = 3,  fg = "blue", font = "Veranda 14 italic bold" , bg="white")
		l4.grid(row=3, column=4)
		plot(r, p)       
		##r=at
		#p=['p1','p2','p3']
	if (alg.get()=="preemtive Priority"):
		r=Prepriority.processData(n,at,bt,pr)
		#print(r)
		#print(p)
		l4 = Label(root, text = avg_wait, padx = 3,  fg = "blue", font = "Veranda 14 italic bold" , bg="white")
		l4.grid(row=3, column=4)
		plot(r, p)
	if (alg.get()=="non_preemtive Priority"):
		r=priority.processData(n,at,bt,pr)
		#print(r)
		#print(p)
		l4 = Label(root, text = avg_wait, padx = 3,  fg = "blue", font = "Veranda 14 italic bold" , bg="white")
		l4.grid(row=3, column=4)
		plot(r, p)
		#r=at
		#p=['p1','p2','p3']



def sec_input():

	label = Label(root, text=p[count - 1], fg = "blue", font = "Veranda 14 bold italic" , bg="white")
	label.grid(row=0, column=2)
	l1 = Label(root, text="Enter the CPU burst", fg = "blue", font = "Veranda 12 italic" , bg="white")
	l1.grid(row=2, column=2)
	e1 = Entry(root)
	e1.grid(row=3, column=2)
	l2 = Label(root, text="Enter the arrival time", fg = "blue", font = "Veranda 12 italic" , bg="white")
	l2.grid(row=5, column=2)
	e2 = Entry(root)
	e2.grid(row=6, column=2)
	if ((alg.get() == "Round Robin") and (count == n)):
		l3 = Label(root, text="Enter the Quantum Time", fg = "blue", font = "Veranda 12 italic" , bg="white")
		l3.grid(row=8, column=2)
		e3 = Entry(root)
		e3.grid(row=9, column=2)
	if (alg.get() == "preemtive Priority"):
		l3 = Label(root, text="Enter the priority from 1 to 5", fg = "blue", font = "Veranda 12 italic" , bg="white")
		l3.grid(row=8, column=2)
		e3 = Entry(root)
		e3.grid(row=9, column=2)
	if (alg.get() == "non_preemtive Priority" ):
		l3 = Label(root, text="Enter the priority from 1 to 5", fg = "blue", font = "Veranda 12 italic" , bg="white")
		l3.grid(row=8, column=2)
		e3 = Entry(root)
		e3.grid(row=9, column=2)
	if (count < n):
		if (alg.get() == "preemtive Priority"):
			b = Button(root, text="Read values",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: read(e1.get(), e2.get(), e3.get()))
			b.grid(row=11, column=2)
		elif (alg.get() == "non_preemtive Priority"):
			b = Button(root, text="Read values",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: read(e1.get(), e2.get(), e3.get()))
			b.grid(row=11, column=2)
		else:
			b = Button(root, text="Read values",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: read(e1.get(), e2.get(), 1))
			b.grid(row=11, column=2)
	elif((alg.get() == "Round Robin") and (count == n)):
		b = Button(root, text="See the output",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: finish(e1.get(), e2.get(), e3.get()))
		b.grid(row=11, column=2)
	elif ((alg.get() == "preemtive Priority") and (count==n)):
		b = Button(root, text="See the output",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: finish(e1.get(), e2.get(), e3.get()))
		b.grid(row=11, column=2)
	elif ((alg.get() == "non_preemtive Priority") and (count==n)):
		b = Button(root, text="See the output",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: finish(e1.get(), e2.get(), e3.get()))
		b.grid(row=11, column=2)
	else:
		b = Button(root, text="See the output",fg = "red", font = "Veranda 12 bold" , bg="white", command=lambda: finish(e1.get(), e2.get(), 1))
		b.grid(row=11, column=2)
		
	l5 = Label(root, text = "Average Waiting time equals :",font = "Veranda 12 bold", padx = 3)
	l5.grid(row=1, column=4)
	


def submit():
	if (num_check() == 0):
		id_generator(p, n)
		if (alg.get() == types[0]):
			sec_input()
		elif (alg.get() == types[1]):
			sec_input()
		elif (alg.get() == types[2]):
			sec_input()
		elif (alg.get() == types[3]):
			sec_input()
		elif (alg.get() == types[4]):
			sec_input()
		elif (alg.get() == types[5]):
			sec_input()

# defining the types of the drop down menu
types = ["Round Robin",
		"FCFS", 
		"preemtive SJF",
		"non_preemtive SJF", 
		"preemtive Priority",
		"non_preemtive Priority"
		]


font = {'family': 'serif',
			'color':  'white',
			'weight': 'bold',
			'size': 16,
			}

count = 1
avg_wait = 0

n = 0 # number of processes

global p # process names in sequence
p = []
global bt # burst time input list
bt = []
global at # arrival time input list
at = []
global pr 
pr=[]
global quantumm


# Creating the main window
root = Tk()
root.title("CPU Scheduler Desktop Application")
root.iconbitmap("images/asu.ico")
root.geometry("1000x550")
root.configure(bg="light blue")
#root.rowconfigure(0, weight=1)


#process_num = entry.get()

alg = StringVar(root)  # For sensing whenever the value is changed
alg.set(types[0])

# Scheduler type selection
typeLabel = Label(root, text="Select Scheduler Type", fg = "blue", font = "Veranda 12" , bg="white")
typeLabel.grid(row=0, column=0)
menu = OptionMenu(root, alg, *types)
menu.grid(row=1, column=0)


# Number of proccesses entry
numLabel = Label(root, text="Enter the number of processes", fg = "blue", font = "Veranda 12" , bg="white")
numLabel.grid(row=4, column=0)
entry = Entry(root)
entry.grid(row=5, column=0)


# button to start excution
start_button = Button(root, text="Start",fg = "blue", font = "Veranda 14 bold italic", command=submit)
start_button.grid(row=8, column=0)

# button to exit the program
exit_button = Button(root, text="Exit Program", fg = "red", font = "Veranda 12 bold italic",command=exit)
exit_button.grid(row=9, column=0)

# Application Text
#txt = Label(root, text="CPU Scheduler Desktop Application", bg="white")
#txt.grid(row=1, column=2, rowspan=3)

# defining the used logo
img = ImageTk.PhotoImage(Image.open("images/asu.png"))  # defining the image
my_label = Label(image=img, bg="light blue") # putting the image into a label
my_label.place(relx = 1.0,rely = 1.0,anchor ='se')
#my_label.grid(row=3, column=3, rowspan=10)



root.mainloop()

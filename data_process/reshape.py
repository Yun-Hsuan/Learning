import numpy as np
import matplotlib.pyplot as plt
import matplotlib as rc
import seaborn as sns 
import os.path
import time
from time import mktime
from datetime import datetime
import collections
import copy

Cap_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ifname = "../tsmc_data/WaferLog.csv"
ifname = "../tsmc_data/WaferLog.csv"
iyfname = "../tsmc_data/Yield.csv"
ifroot = "../tsmc_data/Tool_log"
ofroot = "../tsmc_data/Tool_log_sort"
isortfroot = "../tsmc_data/Tool_log_sort"
ofpname = "wafer_buf_expand.csv"

def get_chamber(dataSet_i):
	
	return dataSet_i[1][-1]

def get_action(dataSet_i):


	term = dataSet_i[7].split("_")
	s = ""
	if len(term) == 2:
		if len(term[0]) == 6:
			if len(term[1]) == 3:
				s = "OC" + get_chamber(dataSet_i)
			elif len(term[1]) == 4:
				s = "OT"
		elif len(term[0]) == 5:
			if len(term[1]) == 3:
				s = "IC" + get_chamber(dataSet_i)
			elif len(term[1]) == 4:
				s = "IT"
	elif len(term) == 3:
		if term[1][0] == 'C':
			if term[2][0] == 'S':
				s = "SCN"
			elif term[2][0] == 'F':
				s = "FCN"
		elif term[1][0] == 'P':
			if term[2][0] == 'S':
				s = "SPM"
			elif term[2][0] == 'F':
				s = "FPM"

	return s 

def load_tool_log(Froot, tool_type, tool_num):

	Fname = Froot + "/ToolLog_Tool_" + tool_type + "_" + str(tool_num) + ".csv"

	dateSet = []
	label   = []

	print Fname

	if os.path.isfile(Fname):

		fp = open(Fname, "r")
		cnt_line = 0;
		for line in fp:
			if cnt_line == 0:
				label = line[:-2].split(",")[1:]
				cnt_line += 1
			else:
				terms = line[:-2].split(",")[1:]
				for i in xrange(len(terms)):
					if terms[i][0] == '"':
						terms[i] = copy.copy(terms[i][1:-1])
				terms[6] = copy.copy(datetime.fromtimestamp(mktime(time.strptime(terms[6], "%Y-%m-%d %H:%M:%S"))))
				dateSet.append(terms)
				#exit()
		fp.close()
	
	else:
		labe1  	= []
		dateSet = []

	return label, dateSet

def load_sort_tool_log(Froot, tool_type, tool_num):

	Fname = Froot + "/ToolLog_Tool_" + tool_type + "_" + str(tool_num) + ".csv"

	dateSet = []
	label   = []

	print Fname

	if os.path.isfile(Fname):

		fp = open(Fname, "r")
		cnt_line = 0;
		for line in fp:
			if cnt_line == 0:
				label = line[:-1].split(",")[1:]
				cnt_line += 1
			else:
				terms = line[:-1].split(",")[1:]
				terms[6] = copy.copy(datetime.fromtimestamp(mktime(time.strptime(terms[6], "%Y-%m-%d %H:%M:%S"))))
				dateSet.append(terms)
				#exit()
		fp.close()
	
	else:
		labe1  	= []
		dateSet = []

	return label, dateSet

def get_detail_tool_log(isortfroot):

	tool_log = dict()

	for c in Cap_letter:

		#if c != 'A':
		#	continue
		cnt_tool_fp = 1
		while(1):

			Fname = isortfroot + "/ToolLog_Tool_" + c + "_" + str(cnt_tool_fp) + ".csv"

			if not os.path.isfile(Fname):
				break

			dateSet = []
			label   = []

			print Fname

			fp = open(Fname, "r")
			cnt_line = 0;


			for line in fp:
				if cnt_line == 0:
					cnt_line += 1
					continue
				else:
					terms = line[:-1].split(",")
					waferName = terms[3]
					action = get_action(terms)
					if waferName[0] != 'N' and not tool_log.has_key(waferName):
						tool_log[waferName] = [ [] for i in xrange(300) ]
					if terms[5][0] != 'N' and action != 'OT':
						stageNum = int(terms[5]) - 1
						#print tool_log[waferName]
						if action == 'IT':
							tool_log[waferName][stageNum].append(terms[4])
						else:
							bufvec = copy.copy(tool_log[waferName][stageNum])	
							#print bufvec
							if len(bufvec) == 1 or bufvec[-4][0] == 'C':
								tool_log[waferName][stageNum] += [terms[1],terms[2],terms[6]]
								#print tool_log[waferName]
							elif bufvec[-3][0] == 'C':
								tool_log[waferName][stageNum].append(terms[6])
					else:
						continue

			fp.close()
			cnt_tool_fp += 1

		#ofp = open("test","w")

		##print Fname
		#tool_log = collections.OrderedDict(sorted(tool_log.items()))

		#for key, val in tool_log.iteritems():
		#	ofp.write( "======2=\n")
		#	ofp.write(key)
		#	for i in xrange(len(val)):
		#		if len(val[i]) == 0:
		#			continue
		#		else:
		#			for j in xrange(len(val[i])):
		#				ofp.write(","+val[i][j])
		#			ofp.write("\n")
		#			
		#ofp.close()
		#exit()

	return tool_log



def load_wafer_log(fname, iyfname, ofname, expand_tool, isortfroot=""):

	ifp = open(fname, "r")
	iyfp = open(iyfname, "r")

	wafer_yield = dict()
	wafer_log = dict()
	stage_log = dict()
	complete_log = dict()

	ofp = open(ofname, "w")

	cnt_line = 0
	for line in iyfp:
		if cnt_line == 0:
			cnt_line += 1
			continue
		terms = line[:-1].replace("\r","").split(",")
		waferName = copy.copy(terms[0])
		assert(not wafer_yield.has_key(waferName))
		wafer_yield[waferName] = terms[1]

	max_stage = 0
	cnt_line = 0
	for line in ifp:
		if cnt_line == 0:
			cnt_line += 1
			continue
		else:			
			terms = line[:-1].split(",")
			waferName = terms[2][1:-1]
			if terms[3][0] == 'N':
				end_t = datetime.fromtimestamp(mktime(time.strptime(terms[6][1:-1], "%Y-%m-%d %H:%M:%S")))
				complete_log[waferName] = end_t
			else:
				if int(terms[3]) > max_stage:
					max_stage = int(terms[3])
				if not wafer_log.has_key(waferName):
					wafer_log[waferName] = dict()
					wafer_log[waferName][int(terms[3])] = [terms[4][1:-1], terms[5][1:-1], terms[6][1:-1]]
				else:
					if not wafer_log[waferName].has_key(int(terms[3])):
						wafer_log[waferName][int(terms[3])] = [terms[4][1:-1], terms[5][1:-1], terms[6][1:-1]]
					else:
						wafer_log[waferName][int(terms[3])].append(terms[6][1:-1])
			
		#cnt_line += 1
		#if cnt_line == 100:
		#	break

	wafer_log = collections.OrderedDict(sorted(wafer_log.items()))
	ofp.write("Wafer.ID,Lot")

	print "Get tool log"
	tool_log = get_detail_tool_log(isortfroot)

	tmp = tool_log["LT0421.01"]

	if not expand_tool:
		for i in xrange(max_stage):
			ofp.write(",stage"+str(i+1)+".Process"+",stage"+str(i+1)+".Tools"+",stage"+str(i+1)+".PTime"+",stage"+str(i+1)+".QTime")
	else:
		for i in xrange(max_stage):
			ofp.write(",stage"+str(i+1)+".Process"+",stage"+str(i+1)+".Tools")
			ofp.write(",stage"+str(i+1)+".slot")
			for j in xrange((len(tmp[i])-1)/4):
				if j == (len(tmp[i])-1)/4 -1:
					ofp.write(",stage"+str(i+1)+".CHB"+str(j+1)+",stage"+str(i+1)+".REP"+str(j+1)+",stage"+str(i+1)+".CP_TIME"+str(j+1))
				else:
					ofp.write(",stage"+str(i+1)+".CHB"+str(j+1)+",stage"+str(i+1)+".REP"+str(j+1)+",stage"+str(i+1)+".CP_TIME"+str(j+1)+",stage"+str(i+1)+".T_TIME"+str(j+1)+str(j+2))
			ofp.write(",stage"+str(i+1)+".PTime"+",stage"+str(i+1)+".QTime")
	ofp.write(",Yield\n")


	for waferName, stages in wafer_log.iteritems():
		if not wafer_yield.has_key(waferName):
			continue	
		stages = collections.OrderedDict(sorted(stages.items()))
		lotName = waferName.split(".")[0]
		last_out_tool_t = 0
		out_time = 0
		ofp.write(waferName+","+lotName)

		for stage, logs in stages.iteritems():

			#out_time = 0
			in_time  = datetime.fromtimestamp(mktime(time.strptime(logs[2], "%Y-%m-%d %H:%M:%S")))
			if stage != 1:
				assert(last_out_tool_t != 0)	
				Q_time = (in_time - last_out_tool_t).total_seconds()
				ofp.write(","+str(int(Q_time)))
			#if len(logs) == 4:
			out_time = datetime.fromtimestamp(mktime(time.strptime(logs[3], "%Y-%m-%d %H:%M:%S")))
			last_out_tool_t = copy.copy(out_time)
			p_time = (out_time - in_time).total_seconds()

			if expand_tool:
				ofp.write(","+logs[0]+","+logs[1])
				#slot, chb, res, cptime, trtime
				buf = tool_log[waferName][stage-1]
				for i in xrange(len(buf)):
					if (i - 1) % 4 == 2:
						pt = (datetime.fromtimestamp(mktime(time.strptime(buf[i+1], "%Y-%m-%d %H:%M:%S")))\
								- datetime.fromtimestamp(mktime(time.strptime(buf[i], "%Y-%m-%d %H:%M:%S")))).total_seconds()
						ofp.write(","+str(int(pt)))
					elif i != 0 and (i - 1) % 4 == 3 and (i+4) < len(buf):
						ct = (datetime.fromtimestamp(mktime(time.strptime(buf[i+3], "%Y-%m-%d %H:%M:%S"))) \
								- datetime.fromtimestamp(mktime(time.strptime(buf[i], "%Y-%m-%d %H:%M:%S")))).total_seconds()
						ofp.write(","+str(int(ct)))
					elif i != len(buf) -1:
						ofp.write(","+buf[i])
				ofp.write(","+str(int(p_time)))
			else:
				ofp.write(","+logs[0]+","+logs[1]+","+str(int(p_time)))
		complete_t = int((complete_log[waferName] - out_time).total_seconds())
		ofp.write(","+str(complete_t)+","+wafer_yield[waferName]+"\n")
		
	#print wafer_log
	#exit()
	ifp.close()
	ofp.close()
	iyfp.close()

def sort_tool_log(ifroot, ofroot):
	
	for c in Cap_letter:
		label = [-2]
		cnt_tool_fp = 1
		while(1):
			ofname = ofroot + "/ToolLog_Tool_" + c + "_" + str(cnt_tool_fp) + ".csv"
			label, tdata = load_tool_log(ifroot, c, cnt_tool_fp)
			if len(label) == 0:
				break
			ofp = open(ofname, "w")
			tdata.sort(key=lambda x: x[6])
			for t in xrange(len(label)):
				if t == 0:
					ofp.write(label[t])
				else:
					ofp.write(","+label[t])
			ofp.write("\n")
			for l in xrange(len(tdata)):
				for i in xrange(len(tdata[l])):
					if i == 0:
						ofp.write(tdata[l][0])
					elif i == 6:
						ofp.write(","+unicode(tdata[l][i]))
					else:
						ofp.write(","+tdata[l][i])
				ofp.write("\n")
				
			cnt_tool_fp += 1
			
			ofp.close()

if __name__ == '__main__':	
	
	#get_detail_tool_log(isortfroot)
	#sort_tool_log(ifroot, ofroot)	
	#tmp, dataSet = load_tool_log(ifroot, 'D', 1)
	#print dataSet[0]
	#exit()
	#max_stage = 3
	#str_qq = ""
	#for i in xrange(max_stage):
	#	 str_qq += ",stage"+str(i+1)+".Process"+",stage"+str(i+1)+".Tools"+",stage"+str(i+1)+".PTime"+",stage"+str(i+1)+".QTime"
	#print str_qq
	#print "\n"
	#exit()
	load_wafer_log(ifname, iyfname, ofpname, True, isortfroot)



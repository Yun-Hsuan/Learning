import numpy as np
import matplotlib.pyplot as plt
import matplotlib as rc
import seaborn as sns 
import os.path
import time
from time import mktime
from datetime import datetime
import collections


Cap_letter= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_chamber(dataSet_i):
	
	return dataSet_i[1][-2]

def get_lot(dataSet_i):

	lot = ""
	
	if not dataSet_i[3] == 'NA':
		lot = dataSet_i[3].split(".")[0][3:]
	else:
		lot = 'NA'

	return lot

def get_wafer(dataSet_i):
	
	wafer = ""

	if not dataSet_i[3] == 'NA':
 		wafer = dataSet_i[3][3:-1]
	else:
		wafer = 'NA'

	return wafer

def get_time(dataSet_i):

	t = time.strptime(dataSet_i[6][1:-1], "%Y-%m-%d %H:%M:%S")
	return datetime.fromtimestamp(mktime(t))

def get_recipe(dataSet_i):

	recipe = ""
	if not dataSet_i[2] == 'NA':
 		recipe = dataSet_i[2][1:-1]
	else:
		recipe = 'NA'

	return recipe
	

def get_stage(dataSet_i):

	return dataSet_i[5]

def get_slot(dataSet_i):

	return dataSet_i[4]

def get_action(dataSet_i):


	term = dataSet_i[7].split("_")
	s = ""
	if len(term) == 2:
		if len(term[0]) == 7:
			if len(term[1]) == 4:
				s = "OC" + get_chamber(dataSet_i)
			elif len(term[1]) == 5:
				s = "OT"
		elif len(term[0]) == 6:
			if len(term[1]) == 4:
				s = "IC" + get_chamber(dataSet_i)
			elif len(term[1]) == 5:
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
				label = line[:-1].split(",")[1:]
				cnt_line += 1
			else:
				dateSet.append(line[:-2].split(",")[1:])
				#print dateSet[-1]
				#exit()
		fp.close()
	
	else:
		labe1  	= []
		dateSet = []

	return label, dateSet
		


def cnt_stage_with_toolX(Froot, tool_type):
	

	stages = []
	cnt_tool = 1
	label = [-2]	
	while( len(label) != 0):
		label, dateSet = load_tool_log(Froot, tool_type, cnt_tool)
		for i in xrange(len(dateSet)):
			if not dateSet[i][5] in stages and dateSet[i][5] != 'NA':
				stages.append(dateSet[i][5])
		cnt_tool += 1

	return stages

def buffer_data(ifroot, ofname):
	
	ofp = open(ofname, "w")

	chambersNums = []
	tool_chambers = []

	sameChamNum_in_sameTool = True

	for c in Cap_letter:
		chamNum_old = -1
		label 	 = [-2]	
		chambers = []
		cnt_tool = 1
		while( len(label) != 0 ):
			label, dateSet = load_tool_log(ifroot, c, cnt_tool)
			for i in xrange(len(dateSet)):
				if not dateSet[i][1][-2] in chambers and not dateSet[i][1][-2] == 'N':
					chambers.append(dateSet[i][1][-2])
			if chamNum_old != len(chambers) and chamNum_old != -1:
				sameChamNum_in_sameTool = False
			if not sameChamNum_in_sameTool:
				print "Fucn: "
				print dateSet[i]
			cnt_tool += 1
		if(len(chambers) != 0):
			chambersNums.append(len(chambers))
			tool_chambers.append(chambers)
			ofp.write(c+","+str(len(chambers))+"\n")
	ofp.close()

	return chambersNums, tool_chambers

def is_sequential(wafer, chamNum):

	cnt_err = 0
	for key, val in wafer.iteritems():
		sequntial = True
		for i in xrange(len(val)/2 - 1):
			if not ((int(val[2*i]) % chamNum )+ 1) == int(val[2*(i+1)]):
				sequntial = False
				break
		if not sequntial:
			cnt_err += 1
			#print (key, val)
	return cnt_err

def cnt_sequential_tool(Froot, bufData):

	ifp = open(bufData, "r")
	ofp = open("seq_error.csv", "w")

	tool_chamNum = dict()
	sequential_tools = []

	for line in ifp:
		terms = line[:-1].split(",")
		tool_chamNum[terms[0]] = int(terms[1])

	for c in Cap_letter:
		wafer = dict()
		label 	 = [-2]	
		cnt_tool = 1
		while( len(label) != 0 ):
			label, dateSet = load_tool_log(ifroot, c, cnt_tool)
			for i in xrange(len(dateSet)):
				if not wafer.has_key(dateSet[i][3]):
					if not dateSet[i][1][-2] == 'N':
						wafer[dateSet[i][3]] = [dateSet[i][1][-2]]
				else:
					if not dateSet[i][1][-2] == 'N':
						wafer[dateSet[i][3]].append(dateSet[i][1][-2])
			cnt_tool += 1
		if(len(wafer) != 0):
			cnt_err = is_sequential(wafer, tool_chamNum[c])
			ofp.write(c+","+str(len(wafer))+","+str(cnt_err)+"\n")
			#sequential_tools.append(c)
	
	ifp.close()
	ofp.close()
	return sequential_tools

def avg_recipe_process_time(ifroot, stage):

	recipe = dict()

	for c in Cap_letter:
		label 	 = [-2]	
		cnt_tool = 1
		while( len(label) != 0 ):
			label, dateSet = load_tool_log(ifroot, c, cnt_tool)
			for i in xrange(len(dateSet)):
				if not wafer.has_key(dateSet[i][5]):
					if not dateSet[i][1][-2] == 'N':
						wafer[dateSet[i][3]] = [dateSet[i][1][-2]]
				else:
					if not dateSet[i][1][-2] == 'N':
						wafer[dateSet[i][3]].append(dateSet[i][1][-2])
			cnt_tool += 1


def transfer_t_chm2chm(ifroot, stageNum, lotName, chm0Lable, chm1Label, ofname):

	ofp = open(ofname, "w")
	wafer = dict()

	for c in Cap_letter:

		if (not c == 'M') and (not c == 'N'):
			continue

		label 	 = [-2]	
		cnt_tool = 1
		while( len(label) != 0 ):
			label, dataSet = load_tool_log(ifroot, c, cnt_tool)
			for i in xrange(len(dataSet)):
				if get_stage(dataSet[i])[0] == 'N' or int(get_stage(dataSet[i])) != stageNum:
					continue
				else:
					if get_lot(dataSet[i]) == lotName:
						wafe_name = get_wafer(dataSet[i])
						if get_action(dataSet[i]) == 'OC1':
							if not wafer.has_key(wafe_name):
								wafer[wafe_name] = [get_time(dataSet[i])]
							else:
								wafer[wafe_name].append(get_time(dataSet[i]))
						elif get_action(dataSet[i]) == 'IC2':
							if not wafer.has_key(wafe_name):
								wafer[wafe_name] = [get_time(dataSet[i])]
							else:
								wafer[wafe_name].append(get_time(dataSet[i]))
			cnt_tool += 1

	#check all wafers
	skip_list = []
	for key, time in wafer.iteritems():
		if len(time) != 2:
			print time
			skip_list.append(key)
	
	oput = collections.OrderedDict(sorted(wafer.items()))

	for key, time in oput.iteritems():
		if key in skip_list:
			continue
		else:
			time.append(time[1]-time[0])
			ofp.write("LT"+key+","+str(time[-1].total_seconds())+"\n")

	ofp.close()

	return wafer, skip_list


def clean_time(ifroot, ofname):

	ofp = open(ofname, "w")
	action_tag = []
	tool_cleant = dict()
	tool_deltat = dict()

	for c in Cap_letter:

		label 	 = [-2]	
		cnt_tool = 1

		while( len(label) != 0 ):
			label, dataSet = load_tool_log(ifroot, c, cnt_tool)
			for i in xrange(len(dataSet)):
				action = get_action(dataSet[i])
				if action == 'SCN' or action == 'FCN':
					if not tool_cleant.has_key(c):
						tool_cleant[c] = {'SCN': [], 'FCN': []} 
					tool_cleant[c][action].append(get_time(dataSet[i]))
			cnt_tool += 1

	for key, val in tool_cleant.iteritems():
		avgt = 0.
		if len(val['SCN']) != len(val['FCN']):
			print "error!!!"
		for i, j in zip(val['SCN'], val['FCN']):
			avgt += float((j - i).total_seconds())
		avgt /= float(len(val['SCN']))
		tool_deltat[key] = avgt

	oput = collections.OrderedDict(sorted(tool_deltat.items()))
	
	for key, val in oput.iteritems():
		ofp.write(key+","+str(val)+"\n")

	ofp.close()

	return tool_deltat

def wafer_per_hour(ifroot, tool_type):

	wafers = []

	while( len(label) != 0 ):
		label, dataSet = load_tool_log(ifroot, tool_type, cnt_tool)
		#detect line by line
		Begin = False
		t0 = 0
		next_t0 = 0
		for i in xrange(len(dataSet)):
			if get_action(dataSet[i]) == 'IT':
				t0 = get_time(dataSet[i])
				Begin = True	
			if Begin:
				if get_action(dataSet[i]) == 'OT':
					buft0 = get_time(dataSet[i])
					Begin = False
					

				waferName = get_wafer(dataSet[i])
				if not waferName in wafers:
					wafers.append(waferNum)
				
		cnt_tool += 1

def recipe_pt(ifroot, stage, ofname):

	ofp = open(ofname, "w")

	wafers = dict()

	rep_time = dict()

	for c in Cap_letter:

		if not c == 'H':
			continue

		label 	 = [-2]	
		cnt_tool = 1

		while( len(label) != 0 ):
			label, dataSet = load_tool_log(ifroot, c, cnt_tool)
			for i in xrange(len(dataSet)):
				if not get_stage(dataSet[i])[0] == 'N' and int(get_stage(dataSet[i])) == 153:
					waferName = get_wafer(dataSet[i])
					recipe = get_recipe(dataSet[i])
					if not wafers.has_key(waferName):
						wafers[waferName] = dict()
					if not recipe == 'NA' and not wafers[waferName].has_key(recipe):
						wafers[waferName][recipe] = []
					if get_action(dataSet[i])[:-1] == 'IC' or get_action(dataSet[i])[:-1] == 'OC':
						wafers[waferName][recipe].append(get_time(dataSet[i]))
						#qq += 1


					#if(qq > 10):
			cnt_tool += 1

		for waf, rep in wafers.iteritems():
			for key, val in rep.iteritems():
				if len(val) != 2:
					print "Error"
					print waf + "," + key
					exit(0)
				else:
					if not rep_time.has_key(key):
						rep_time[key] = [.0, .0]
					if (val[1] - val[0]).total_seconds() < 0:
						print "Error"
						print waf + "," + key
					rep_time[key][0] += 1
					rep_time[key][1] += (val[1] - val[0]).total_seconds()
					
		oput = collections.OrderedDict(sorted(rep_time.items()))
		for key, val in oput.iteritems():
			ofp.write(key+","+str(val[1]/val[0])+"\n")

		return rep_time

def max_lot_b4PM(ifroot, tool_type, ofname):

	ofp = open(ofname, "w")

	label 	 = [-2]	
	cnt_tool = 1
	max_num = -1
	cn = 1

	while( len(label) != 0 ):

		lots  = []
		label, dataSet = load_tool_log(ifroot, tool_type, cnt_tool)
		Begin = False
		for i in xrange(len(dataSet)):
			if get_action(dataSet[i]) == 'FPM':
				Begin = True
			if Begin:
				if get_action(dataSet[i]) == 'SPM':
					Begin = False
					if max_num < len(lots):
						max_num = len(lots)
					lots = []
				else:
					lotName = get_lot(dataSet[i])
					if not lotName in lots and not lotName == 'NA':
						lots.append(lotName)

		cnt_tool += 1

	ofp.write(tool_type+","+str(max_num)+"\n")
	ofp.close()

	return max_num
	
def tool_pm_fixLot(ifroot, ofname):

	ofp = open(ofname, "w")

	tools = []

	for c in Cap_letter:

		if not c == 'H':
			continue

		label = [-2]
		cnt_tool = 1
		lotNum = []

		while( len(label) != 0 ):
		
			lots  = []
			label, dataSet = load_tool_log(ifroot, c, cnt_tool)
			Begin = False
			for i in xrange(len(dataSet)):
				if get_action(dataSet[i]) == 'FPM':
					Begin = True
				if Begin:
					if get_action(dataSet[i]) == 'SPM':
						Begin = False
						#print len(lots)
						lotNum.append(len(lots))
						lots = []
					else:
						lotName = get_lot(dataSet[i])
						if not lotName in lots and not lotName == 'NA':
							lots.append(lotName)
				
			cnt_tool += 1

		print lotNum

	ofp.close()

	return tools


if __name__ == '__main__':

	ifroot = "../tsmc_data/Tool_log"

	#load_tool_log(Froot, 'A', 1)
	#Q1: How many stages utilize A-type tool and How many stages utilize G-type tools?
	#stagesA = cnt_stage_with_toolX(ifroot, 'A')
	#stagesG = cnt_stage_with_toolX(ifroot, 'G')
	#print stagesA
	#print "Tool_A: " + str(len(stagesA))
	#print stagesG
	#print "Tool_G: " + str(len(stagesG))

	#ofname = "chamebersNum.csv"
	#chamberNums, chambers = buffer_data(ifroot, ofname)
	#print chamberNums
	#print chambers
	#sequential_tools = cnt_sequential_tool(ifroot, ofname)
	#print sequential_tools

	#Q3:
	#ofname = "Q3"
	#rep_time = recipe_pt(ifroot, 153, ofname)
	#print rep_time

	#Q4:
	#ofname = "Q4"
	#transfer_t, skip_list = transfer_t_chm2chm(ifroot, 279, '0310', 1, 2, ofname
	#print transfer_t	

	#Q5:
	ofname = "Q5buf"
	max_tool_H = max_lot_b4PM(ifroot, 'H', ofname)
	max_tool_J = max_lot_b4PM(ifroot, 'J', ofname)

	print "H," + str(max_tool_H)
	print "J," + str(max_tool_J)
	
	#Q6

	#Q7
	#ofname  = 'Q7'
	#action_tag = clean_time(ifroot, ofname)
	#print action_tag

	#Q8
	#ofname = "Q8"
	#tools = tool_pm_fixLot(ifroot, ofname)
	#print tools


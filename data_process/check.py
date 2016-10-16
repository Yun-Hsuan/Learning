fp = open("./wafer_buf_expand.csv", "r")

old_size = 0
cnt_line = 0
for line in fp:
	if cnt_line == 0:
		old_size = len(line[:-1].split(","))
	else:
		if len(line[:-1].split(",")) != old_size:
			print "Bug, Line: " + str(cnt_line+1) 
			print "len: " + str(len(line[:-1].split(","))) + ",Old: " + str(old_size)
	cnt_line += 1


fp.close()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

def write_N_wafer(df, n):

	sub_df = shuffle(df)[:n]

	sub_df.to_csv("ggdata_"+str(n)+".csv", index=False,index_label=False)

	#return sub_df

def split_N_by_M(df, N, M):

	tmp = shuffle(df)
	inputNum = len(tmp)
	trainNum = (inputNum/(N+M)) * N
	sub1 = tmp[:trainNum]
	sub2 = tmp[trainNum:]

	sub1.to_csv("../ggdata/ggdata_train_"+str(N)+str(M)+".csv", index=False,index_label=False)
	sub2.to_csv("../ggdata/ggdata_test_"+str(N)+str(M)+".csv", index=False,index_label=False)

if __name__ == '__main__':	

	n = 1000

	N = 4
	M = 1

	df = pd.read_csv('../ggdata/ggdata_full.csv')

	#write_N_wafer(df, n)

	split_N_by_M(df, N, M)


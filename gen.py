from random import randint
from heapq import merge
import itertools
import math
import random

def gen_samples(n,T,bound):
	strats = [[]]*n
	for i in range(n):
		m_cste = randint(1, bound)
		m_i = [int(1000*random.random()) for i in range(0,T)]
		m_matrix = [[[random.random() for j in range(nb,T)] for nb in range(i+1)] for i in range(T-1)]
		strats[i] = [m_cste,m_i,m_matrix]
	return strats
    #m_matrix[i][nb][j-nb]
	#bid = m_cste + m_i[i] + sum(m_matrix[i][nb][j-nb] * v[j] for j in range(nb,T))
def gvalue(strats,T,v1,v2):
	m_cste = strats[0][0]
	m_i = strats[0][1]
	m_matrix = strats[0][2]
	#values for the second strat
	m_cste2 = strats[1][0]
	m_i2 = strats[1][1]
	m_matrix2 = strats[1][2]
	winner = 0
	win = [0]*T 
	bid1 = [0]*T
	bid2 = [0]*T
	price = [0]*T
	finalwinner = 0
	nb_1 = 0
	nb_2 =0
	utility_1 = 0
	utility_2 = 0
	#bids
	for i in range(T):
		if (i < T-1):
			bid1[i] = (m_cste + m_i[i] + sum(m_matrix[i][nb_1][j-nb_1] * v1[j] for j in range(nb_1,T)))
			bid2[i] = (m_cste2 + m_i2[i] + sum(m_matrix2[i][nb_2][j-nb_2] * v2[j] for j in range(nb_2,T)))
		else:
			bid1[T-1] = v1[nb_1]
			bid2[T-1] = v2[nb_2]
		price[i] = min(bid1[i], bid2[i])
		winner = 1*(bid1[i] > bid2[i]) + 2*(bid1[i] < bid2[i])
		win.append(winner)
		if (winner == 0):
			winner = random.randint(1,2)
		if (winner == 1):
			nb_1 += 1
			utility_1 += v1[nb_1] - price[i] 
		else:
			nb_2 += 1
			utility_2 += (v2[nb_2] - price[i])
	return utility_1, utility_2

def game(strats, T):
	#values for the first strat
	winner = [[]]*len(strats)
	v1 = [0] + sorted([random.randint(0,2*T) for i in range(T)], reverse = True)
	v2 = [0] + sorted([random.randint(0,2*T) for i in range(T)], reverse = True)
	x1 , y1 = gvalue(strats,T,v1,v2) 
	x2 , y2 = gvalue(strats,T,v2,v1) 
	x3, y3 = gvalue(strats,T,v1,v1)
	x4, y4 = gvalue(strats,T,v2,v2)
	x = x1 + x2 + x3 + x4
	y = y1 + y2 + y3 + y4
	if (x > y):
		winner = 0
	else:
		winner = 1
	return winner

def tournament(strats, tries, T):
	strats_real = strats.copy()
	val = [0 for i in range(len(strats))]

	strats = [i for i in range(len(strats))]
	for j in range(int(math.log(len(strats),2))):
		winner = [[]] * int(len(strats)/2)
		for i in range(int(len(strats)/2)):
			win = game([strats_real[strats[2*i]],strats_real[strats[2*i+1]]], T)
			if(win == 1):
				winner[i] = strats[2*i]
			else:
				winner[i] = strats[2*i+1]
		strats = winner
		for i in winner:
			val[i] = j+1
	return val
def order(strats, fit):
	list1, list2 = (list(t) for t in zip(*sorted(zip(fit, strats))))
	return list2

def gen_new(ordered_strats,n,T,bound):
	half = int(n/2)
	strats = [[]]*half
	pan1 = 0
	pan2 = 0
	for r in range(half):
		pan1 = int((math.sqrt(random.random())*n/2)+n/2)
		pan2 = int((math.sqrt(random.random())*n/2)+n/2)
		x = random.uniform(0, 2)
		if (x < 1):
			m_cste = (ordered_strats[pan1][0] + ordered_strats[pan2][0])/2
		else:
			m_cste = randint(1, bound)

		m_i = [0]*T
		for i in range(0,T):
			if (x < 1):
				m_i[i] = ((ordered_strats[pan1][1][i] + ordered_strats[pan2][1][i])/2)
			else:
				m_i[i] = (1000*random.random())
		if (x < 1):
			m_matrix = [[[((ordered_strats[pan1][2][i][nb][j-nb] + ordered_strats[pan2][2][i][nb][j-nb])/2) for j in range(nb,T)] for nb in range(i+1)] for i in range(T-1)]
		else:
			m_matrix = [[[random.random() for j in range(nb,T)] for nb in range(i+1)] for i in range(T-1)]

		strats[r] = [m_cste,m_i,m_matrix]
	return strats


def fusion(ordered_strats, new_strats):
	n = len(new_strats)
	strats_new = ordered_strats[:n]
	strats_f = list(merge(strats_new, new_strats))
	random.shuffle(strats_f)
	shuffled_strats = strats_f
	return shuffled_strats

def write_log (j, strats, ordered_strats):
	print(j)
	print(ordered_strats[-3:])

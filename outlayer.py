from gen import *
from random import randint
from heapq import merge
import math
import random
n=4
T = 2 
bound = 8
tries = 4
strats = gen_samples(n,T,bound)
rate_log = 8 
j = 0
i = 0
while(j < 100):
    j += 1
    for i in range(rate_log):
    	fit = tournament(strats, tries, T)
    	ordered_strats = order(strats,fit)
    	new_strats = gen_new(ordered_strats,n,T,bound)
    	strats = fusion(ordered_strats, new_strats)

    write_log(j,strats,ordered_strats)
        
        

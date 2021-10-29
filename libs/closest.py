import numpy as np 
def closest(lst, K): 
      
     lst = np.asarray(lst) 
     idx = (np.abs(lst - K)).argmin() 
     return lst[idx] 
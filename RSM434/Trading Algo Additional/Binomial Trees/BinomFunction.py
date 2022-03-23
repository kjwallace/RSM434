import numpy as np

def BinomTree_Maker(Rate, S, K, Divs, sigma, Type, Time, Periods, Up, Down):
    h = 1/Periods
    ret_Tree = [S]
    
    if Up == 0:
        Up = np.exp((Rate - Divs)*h + sigma*np.sqrt(h))
    if Down == 0:
        Down = np.exp((Rate - Divs)*h - sigma*np.sqrt(h))
    
    Beg = 0
    for i in range(Periods):
        End = len(ret_Tree)
        for j in range(Beg,End):
            ret_Tree += [ret_Tree[j]*Up]
            ret_Tree += [ret_Tree[j]*Down]
        Beg = End
    '''print(ret_Tree)'''
    
    '''Price Finding'''
    
        
    x = [ret_Tree[0]]
  
    for g in range(Periods):
        Beg2 = ((2**(g+1)) -1)
        End2 = ((2**(g+2)) -1)
        x += [ret_Tree[Beg2:End2]]
        
      

    return ret_Tree, x
       


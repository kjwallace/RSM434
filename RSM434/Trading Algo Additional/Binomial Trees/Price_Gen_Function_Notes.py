def PriceGenerator(S_Nodes, Up, Down, sigma, Rate, K, Periods, Divs, Type):
    h = 1/Periods
    if Up == 0:
            Up = np.exp((Rate - Divs)*h + sigma*np.sqrt(h))
    if Down == 0:
        Down = np.exp((Rate - Divs)*h - sigma*np.sqrt(h))
        
    Final_Prices = S_Nodes
    Deltas = S_Nodes
    B_Vector = S_Nodes
    Dif = Up - Down
    n = Periods
   
    
    if Type == 1:
        Final_Prices = [a - K for a in Final_Prices]
        for a in range(len(Final_Prices)):
            if Final_Prices[a] < 0:
                Final_Prices[a] = 0
    
                
    else:
        Final_Prices = [K - a for a in Final_Prices]
        for a in range(len(Final_Prices)):
            if Final_Prices[a] < 0:
                Final_Prices[a] = 0
    
    for i in range(Periods,0,-1):
        Beg = 2**(i-1)-1
        End = 2**n - 1
        for j in range(Beg, End):
            Deltas[j] = np.exp(-Divs*h)*(Final_Prices[2*j+1]-Final_Prices[2*j+2])/Dif
            B_Vector[j] = np.exp(-Rate*h)*(Up*Final_Prices[2*j+2] - Down*Final_Prices[2*j+1])/Dif
            Final_Prices[j] = Deltas[j] + B_Vector[j]
    for i in range(len(S_Nodes)):
        if i < 2**n -1:
            Deltas[i] = Deltas[i]/S_Nodes[i]
        else:
            Deltas[i] = 0 
            B_Vector[i] = 0
        
    Del = []
  
    B = [] 
    
    Prices = []
   
    
    for g in range(Periods):
        Beg2 = ((2**(g+1)) -1)
        End2 = ((2**(g+2)) -1)
        Del += [Deltas[Beg2:End2]]
        B += [B_Vector[Beg2:End2]]
        Prices += [Final_Prices[Beg2:End2]]
    
    return Prices, Del, B
units = float(input(" Please enter Number of Units you Consumed : "))
totalslab = int(input(" Please enter Total Number of slab : "))         #asking total categories
slab=[]
rate=[]
totalvalue=[]
us=0
for i in range(totalslab-1):
    unitslab = float(input(" Please enter Number" +str(i+1)+  "Unit slab: " ))
    slab.append(unitslab)
for i in range(totalslab):
    tarrifslab = float(input(" Please enter Number" +str(i+1) + "Tarrif slab rate: " ))
    rate.append(tarrifslab) 
if units<slab[0]:
    amount=units*rate[0]
    print(amount)
else:
    for i in range(len(rate)):
        if i< totalslab-1:
            us=slab[i]+us
            amount = (slab[i]) * (rate[i])
            totalvalue.append(amount)
        if i==totalslab-1:
            unit = (units-us)*(rate[totalslab-1])
            totalvalue.append(unit)
    x=0
    for i in totalvalue:    
        x=x+i
    print(x)
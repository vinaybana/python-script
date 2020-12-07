units = int(input(" Please enter Number of Units you Consumed : "))
totalslab = int(input(" Please enter Total Number of slab : "))            #asking total categories
totalvalue=[]
am=0
us=0
for i,k in enumerate(range(1,totalslab+1)):    
    if i< (totalslab-1):    
        unitslab = int(input(" Please enter Number" +str(k)+  "Unit slab: " ))
        tarrifslab = int(input(" Please enter Number" +str(k) + "Tarrif slab rate: " ))
        us=unitslab+us
        amount = (unitslab * tarrifslab)
        am=amount+am
        totalvalue.append(amount)
    if i==(totalslab-1):
        tarrifslab = int(input(" Please enter Number" +str(k) + "Tarrif slab rate: " ))
        unit = (units-us)*tarrifslab
        totalvalue.append(unit)
x=0
for i in totalvalue:    
    x=x+i
print(x)
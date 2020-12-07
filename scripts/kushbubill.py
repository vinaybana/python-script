#program for calculating electricity bill in Python
totalUnit = float(input("please enter the number of Total Unit you consumed in a month:-"))
count = int(input("Please enter the number of Consumer Category:-"))
uslab = []
pslab = []
for i in range(count-1):
	unitSlab = int(input("please enter "+str(i+1)+" unit Slab:-"))
	uslab.append(unitSlab)
for i in range(count-1):
	priceSlab = int(input("please enter price for "+str(i+1)+" unit slab:-"))
	pslab.append(priceSlab)
priceSlab = int(input("please enter price for remaining units:-"))
pslab.append(priceSlab)
totalprice = 0
for i in range(len(uslab)):
	if(totalUnit > 0):
		if (totalUnit >= uslab[i]):
			totalprice = totalprice + uslab[i] * pslab[i]
			totalUnit = totalUnit - uslab[i]
		else:
			totalprice = totalprice + totalUnit * pslab[i]
			totalUnit = totalUnit - uslab[i]
			break
if(totalUnit > 0):
	totalprice = totalprice + totalUnit * pslab[(len(pslab)-1)]
print(totalprice)
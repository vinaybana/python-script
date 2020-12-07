m_unit,tarrif,total,new_list,break_unit = [],[],0,[],[]
mon_l = int(input("Enter number of monthly slab: "))
for i in range(mon_l):
	m_unit.append(int(input("Enter slab unit {0}: ".format(i+1))))
for i in range(mon_l+1):
	if len(m_unit) == i:
		tarrif.append(int(input("Enter tarrif/rate for units > {0}: ".format(sum(m_unit)))))
	else:
		tarrif.append(int(input("Enter tarrif/rate for {0}-{1}: ".format(0 if i == 0 else sum(m_unit[:i]),m_unit[i] if i == 0 else sum(m_unit[:i+1])))))
unit = float(input("Enter total units: "))
for i in range(mon_l):
	new_list.append(sum(m_unit[:i+1]))
for i in range(len(tarrif)):
	try:
		if unit > m_unit[i]:
			unit = unit-m_unit[i]
			if unit <= 0:
				break
			break_unit.append(m_unit[i])
	except:
		break_unit.append(unit)
for u in range(len(break_unit)):
	total += break_unit[u]*tarrif[u]
print("Total Bill: "+str(total))
from smath.local_params import number_of_symbols

abducibles = []
for j in range(0,10):
    abducibles.append('at({},{})'.format(j,1))

for j in range(1,4):
    abducibles.append('at({},{})'.format(j,2))
        
for j in range(0,10):
    abducibles.append('at({},{})'.format(j,3))

if number_of_symbols == 5:
    for j in range(1,4):
        abducibles.append('at({},{})'.format(j,4))
        
    for j in range(0,10):
        abducibles.append('at({},{})'.format(j,5))
    
        
exclusive = []
me = list()
for j in range(0,10):
    me.append('at({},{})'.format(j,1))
exclusive.append(me)

me = list()   
for j in range(1,4):
    me.append('at({},{})'.format(j,2))
exclusive.append(me)

me = list()
for j in range(0,10):
    me.append('at({},{})'.format(j,3))
exclusive.append(me)

if number_of_symbols == 5:
    me = list()   
    for j in range(1,4):
        me.append('at({},{})'.format(j,4))
    exclusive.append(me)
    
    me = list()
    for j in range(0,10):
        me.append('at({},{})'.format(j,5))
    exclusive.append(me)

abducibles = []
for i in range(1,6):
    for j in range(0,4):
        abducibles.append('at({},{})'.format(j,i))
        
exclusive = []
for i in range(1,6):
    me = list()
    for j in range(0,4):
        me.append('at({},{})'.format(j,i))
    exclusive.append(me)
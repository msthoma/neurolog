
abducibles = []
for i in range(1,5):
    for j in range(0,10):
        abducibles.append('at({},{})'.format(j,i))
        
exclusive = []
for i in range(1,5):
    me = list()
    for j in range(0,10):
        me.append('at({},{})'.format(j,i))
    exclusive.append(me)
        
for i in range(5,9):
    for j in range(1,4):
        abducibles.append('at({},{})'.format(j,i))

for i in range(5,9):
    me = list()
    for j in range(1,4):
        me.append('at({},{})'.format(j,i))
    exclusive.append(me)
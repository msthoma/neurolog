from chess.local_params import pieces

abducibles = []
for i in range(1,4):
    for j in range(1,4):
        for piece in pieces:
            abducibles.append('at({},({},{}))'.format(piece,i,j))
        
exclusive = []
for i in range(1,4):
    for j in range(1,4):
        me = list()
        for piece in pieces:
            me.append('at({},({},{}))'.format(piece,i,j))
        exclusive.append(me)

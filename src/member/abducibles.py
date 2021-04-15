from src.member.local_params import number_of_arguments

abducibles = []
for i in range(1, number_of_arguments + 1):
    for j in range(0, 10):
        abducibles.append('at({},{})'.format(j, i))

exclusive = []
for i in range(1, number_of_arguments + 1):
    me = list()
    for j in range(0, 10):
        me.append('at({},{})'.format(j, i))
    exclusive.append(me)

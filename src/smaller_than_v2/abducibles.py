abducibles = []
for i in range(1, 2 + 1):
    for j in range(0, 10):
        abducibles.append('at({},{})'.format(j, i))

exclusive = []
for i in range(1, 2 + 1):
    me = list()
    for j in range(0, 10):
        me.append('at({},{})'.format(j, i))
    exclusive.append(me)

if __name__ == '__main__':
    print(abducibles)
    print(exclusive)

from typing import List

def parseSicstusProof(line:str):
    abducibles = list()
    cont = True
    while cont == True:
        start = line.find('at', 0)
        if start == -1: 
            cont = False
        else: 
            end = line.find('))', 0)
            abducible = line[start:end+2]
            abducibles.append(abducible)
            line = line[end+2:]
    return abducibles

def importSicstusProofs(fileName:str)->List:
    proofs = list()
    fp = open(fileName, 'r')
    for line in fp:
        line = line.rstrip("\n")
        if line.startswith(' <= '):
            proofs.append(parseSicstusProof(line))
    return proofs  

def convertProofsToTuples(proofs:List):
    tuples = list()
    for proof in proofs:
        W1 = '' 
        W2 = ''
        for abducible in proof:
            colour = abducible[len('at') + 1]
            piece = abducible[len('at') + 3]
            x = int(abducible[len('at') + 7])
            y = int(abducible[len('at') + 9])  
            if colour == 'w':
                if W1 == '':
                    W1 = piece
                    (X1,Y1) = (x,y)
                else:
                    W2 = piece
                    (X2,Y2) = (x,y)
            else:
                (X3,Y3) = (x,y)
        tuples.append((W1,X1,Y1,W2,X2,Y2,X3,Y3))
    return tuples    
    

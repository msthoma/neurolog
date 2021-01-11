from chess.chess_configuration import ChessConfiguration
from params import proofs_root

pieces = ['e','b(k)','w(r)','w(b)','w(n)','w(k)','w(p)','w(q)']
piecesToPosition = dict()
piecesToPosition['e'] = 0
piecesToPosition['bk'] = 1
piecesToPosition['r'] = 2
piecesToPosition['b'] = 3
piecesToPosition['n'] = 4
piecesToPosition['k'] = 5
piecesToPosition['p'] = 6
piecesToPosition['q'] = 7

chess = ChessConfiguration(3, 3, proofs_root, piecesToPosition)
% ---------------- Mini Chess ----------------
% ++++++++++++++++++++++++++++++++++++++++++++

builtin(user:track(_,_)).
%track(Cond,X) :- user:track(Cond,X).
track(_,_).

% ------------- inputs and abducibles --------

% prolog:set_current_directory('C:/Users/Administrator/Documents/academic/software/Abduction/A-System').
% [abduction], [prepare], go.

abducible(at(_,(_,_))).
abducible(cost(_)).

% ------------- neural knowledge -------------

% symbolic factual knowledge of what the neural part sees!

builtin(user:switch(_,_,_)).
switch(N,O,V) :- user:switch(N,O,V).
builtin(user:in_pieces(_)).
in_pieces(ATs) :- user:in_pieces(ATs).
in_piece(AT) :- in_pieces(ATs), member(AT,ATs).
builtin(user:in_empties(_)).
in_empties(EMs) :- user:in_empties(EMs).
in_empty(EM) :- in_empties(EMs), member(EM,EMs).
builtin(user:perturb(_,_)).
perturb(Conf,Cost) :- user:perturb(Conf,Cost).
builtin(user:eval(_,_,_,_)).
eval(A,B,OP,C) :- user:eval(A,B,OP,C).

label(Label) :-
   track(1,1),
   switch(mincost,set,_),
   track(1,2),
   perturb(Conf,Cost), track(1,conf(Conf)),
   switch(mincost,get,Cost), track(1,Cost),
   prove(Label,Conf), track(1,proved),
   fill_conf(Conf,Cost),
   switch(mincost,set,Cost).

prove(safe,Conf) :- safe(Conf).
prove(draw,Conf) :- draw(Conf).
prove(mate,Conf) :- mate(Conf).

fill_conf((PZ,[(PZ1,w(P1)),(PZ2,w(P2))]),Cost) :-
   at(b(k),PZ), at(w(P1),PZ1), at(w(P2),PZ2), cost(Cost).

fill_seen(NZs) :-
   in_pieces(ATs),
   commit(NZs,ATs),
   in_empties(EMs),
   commit(NZs,EMs).

commit(_NZs,[]).
commit(NZs,[empty(Z)|EMs]) :-
   member(Z,NZs),
   commit(NZs,EMs).
commit(NZs,[at(_,Z)|ATs]) :-
   member(Z,NZs),
   commit(NZs,ATs).
commit(NZs,[empty(Z)|EMs]) :-
   \+ member(Z,NZs), empty(Z),
   commit(NZs,EMs).
commit(NZs,[at(?,Z)|ATs]) :-
   \+ member(Z,NZs), full(Z),
   commit(NZs,ATs).
commit(NZs,[at(P,Z)|ATs]) :-
   \+ member(Z,NZs), piece(P), at(P,Z),
   commit(NZs,ATs).


% conflicted_seen([]) :- in_piece(at(P1,Z1)), in_piece(at(_,Z2)), reachable(Z2,P1,Z1), track(seen,at(P1,Z1)>at('?',Z2)).
% conflicted_flip([Z1]) :- in_piece(at(_,Z1)), in_piece(at(_,Z2)), piece(P1), reachable(Z2,P1,Z1), atnew(P1,Z1), track(flip,at(P1,Z1)>at('?',Z2)).
% conflicted_more([Z2]) :- in_piece(at(P1,Z1)), pos(Z2), reachable(Z2,P1,Z1), piece(P2), atnew(P2,Z2), track(more,at('?',Z2)<at(P1,Z1)).
% conflicted_more([Z2]) :- in_piece(at(_,Z1)), piece(P2), pos(Z2), reachable(Z1,P2,Z2), atnew(P2,Z2), track(more,at(P2,Z2)>at('?',Z1)).
% conflicted_pair([Z1,Z2]) :- piece(P1), pos(Z1), pos(Z2), reachable(Z2,P1,Z1), piece(P2), atnew(P1,Z1), atnew(P2,Z2), track(pair,at(P1,Z1)>at('?',Z2)).



% ------------- domain knowledge -------------

builtin(user:pos(_)).
pos(Z) :- user:pos(Z).
builtin(user:dist(_)).
dist(D) :- user:dist(D).
builtin(user:piece(_)).
piece(P) :- user:piece(P).

safe((PZ,Ws)) :- track(2,safeQ(PZ,Ws)), movable(PZ,Ws), track(2,ok).
draw((PZ,Ws)) :- track(2,drawQ(PZ,Ws)), \+attacks(Ws,PZ), track(2,ok1), \+movable(PZ,Ws), track(2,ok2).
mate((PZ,Ws)) :- track(2,mateQ(PZ,Ws)), attacks(Ws,PZ), track(2,ok1), \+movable(PZ,Ws), track(2,ok2).

movable(PZ,Ws) :- pos(Z), track(3,movekingQ(Z)), reachable(Z,k,PZ), track(3,ok1), \+attacks(Ws,Z), track(3,ok2).
attacks(Ws,Z) :- member((PZ,w(P)),Ws), track(4,attackedQ(Z,PZ,w(P))), Z\=PZ, at(w(P),PZ), track(4,ok1), reachable(Z,P,PZ), track(4,ok2).

reachable((X,Y),k,(PX,PY)) :- eval(X,PX,abs,DX), 1 >= DX, eval(Y,PY,abs,DY), 1 >= DY, eval(DX,DY,sum,S), 0 < S.
reachable((X,Y),q,(PX,PY)) :- reachable((X,Y),r,(PX,PY)).
reachable((X,Y),q,(PX,PY)) :- reachable((X,Y),b,(PX,PY)).
reachable((X,Y),r,(PX,PY)) :- eval(X,PX,abs,DX), eval(Y,PY,abs,0), \+blockedX(DX,(X,Y),r,(PX,PY)).
blockedX(DX,(X,Y),r,(PX,PY)) :- dist(M), 0 < M, M < DX, eval(X,PX,min,MX), eval(MX,M,sum,X1), Y1 = PY, piece(P1), at(P1,(X1,Y1)).
reachable((X,Y),r,(PX,PY)) :- eval(X,PX,abs,0), eval(Y,PY,abs,DY), \+blockedY(DY,(X,Y),r,(PX,PY)).
blockedY(DY,(X,Y),r,(PX,PY)) :- dist(M), 0 < M, M < DY, X1 = PX, eval(Y,PY,min,MY), eval(MY,M,sum,Y1), piece(P1), at(P1,(X1,Y1)).
reachable((X,Y),b,(PX,PY)) :- eval(X,PX,abs,D), eval(Y,PY,abs,D), \+blockedD(D,(X,Y),b,(PX,PY)).
blockedD(D,(X,Y),b,(PX,PY)) :- dist(M), 0 < M, M < D, eval(X,PX,min,MX), eval(MX,M,sum,X1), eval(Y,PY,min,MY), eval(MY,M,sum,Y1), piece(P1), at(P1,(X1,Y1)).
reachable((X,Y),n,(PX,PY)) :- eval(X,PX,abs,2), eval(Y,PY,abs,1).
reachable((X,Y),n,(PX,PY)) :- eval(X,PX,abs,1), eval(Y,PY,abs,2).
reachable((X,Y),p,(PX,PY)) :- eval(X,PX,abs,1), eval(Y,PY,abs,1), Y>PY.

ic :- piece(P), at(P,PZ1), at(P,PZ2), PZ1\=PZ2.
ic :- piece(P1), piece(P2), at(P1,PZ), at(P2,PZ), P1\=P2.
ic :- at(b(k),PZ1), at(w(k),PZ2), reachable(PZ1,k,PZ2).
ic :- piece(b(P1)), at(b(P1),PZ1), piece(b(P2)), at(b(P2),PZ2), PZ1\=PZ2.
ic :- piece(w(P1)), at(w(P1),PZ1), piece(w(P2)), at(w(P2),PZ2), piece(w(P3)), at(w(P3),PZ3), PZ1\=PZ2, PZ2\=PZ3, PZ3\=PZ1.

% --------------------------------------------
% ---------------- Basic Dom -----------------
% ++++++++++++++++++++++++++++++++++++++++++++

builtin(user:track(_,_)).
%track(Cond,X) :- user:track(Cond,X).
track(_,_).

% ------------- inputs and abducibles --------

% prolog:set_current_directory('C:/Users/Administrator/Documents/academic/software/Abduction/A-System').
% [abduction], [prepare], go.


builtin(user:sidefeed(_)).
sidefeed(SF) :- user:sidefeed(SF).

abducible(at(_,_)).
label([R1, R2, C1, C2]) :- operator2x2(R1, R2, C1, C2).

% ------------- domain knowledge -------------

digit(N) :- N in 0..9.
op(N) :- N in 1..3.

operator2x2(R1, R2, C1, C2) :-
   digit(D1), at(D1,1),
   digit(D2), at(D2,2),
   op(S1), at(S1,5),
   aux(D1,S1,D2,R1),
   digit(D3), at(D3,3),
   digit(D4), at(D4,4),
   op(S2), at(S2,6),
   aux(D3,S2,D4,R2),
   op(S3), at(S3,7),
   op(S4), at(S4,8),
   aux(D1,S3,D3,C1),
   aux(D2,S4,D4,C2).

aux(D1,1,D2,Z) :- Z #= (D1 + D2).
aux(D1,2,D2,Z) :- Z #= (D1 - D2).
aux(D1,3,D2,Z) :- Z #= (D1 * D2).
 

% --------------------------------------------



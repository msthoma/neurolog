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
label([R]) :- math(R).

% ------------- domain knowledge -------------

digit(N) :- N in 0..9.
op(N) :- N in 1..3.

math(R) :-
   digit(D1), at(D1,1),
   digit(D3), at(D3,3),
   op(O1), at(O1,2),
   aux(D1,O1,D3,R).

aux(D1,1,D2,Z) :- Z #= (D1 + D2).
aux(D1,2,D2,Z) :- Z #= (D1 - D2).
aux(D1,3,D2,Z) :- Z #= (D1 * D2).
 
% --------------------------------------------



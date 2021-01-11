% ---------------- Basic Dom -----------------
% ++++++++++++++++++++++++++++++++++++++++++++

builtin(user:track(_,_)).
%track(Cond,X) :- user:track(Cond,X).
track(_,_).

% ------------- inputs and abducibles --------

% prolog:set_current_directory('C:/Users/Administrator/Documents/academic/software/Abduction/A-System').
% [abduction], [prepare], go.

abducible(at(_,_)).
builtin(user:sidefeed(_)).
sidefeed(SF) :- user:sidefeed(SF).

label([Row1, Row2, Col1, Col2]) :- add2x2(Row1, Row2, Col1, Col2).

% ------------- domain knowledge -------------

digit(N) :- N in 0..9.

add2x2(Row1, Row2, Col1, Col2) :-
   digit(D1), at(D1,1),
   digit(D2), at(D2,2),
   Row1 #= D1+D2,
   digit(D3), at(D3,3),
   Col1 #= D1+D3,
   digit(D4), at(D4,4),
   Row2 #= D3+D4,
   Col2 #= D2+D4.

% --------------------------------------------
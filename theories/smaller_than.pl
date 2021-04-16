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
label([Second,Z]) :- smaller(Second,Z).

% ------------- domain knowledge -------------

digit(N) :- N in 0..9.

smaller(Second,Z) :- digit(First), at(First,1), digit(Second), at(Second,2), First #< Second, Z #= 1.
smaller(Second,Z) :- digit(First), at(First,1), digit(Second), at(Second,2), First #>= Second, Z #= 0.

% --------------------------------------------



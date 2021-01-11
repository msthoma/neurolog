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
label([D,Z]) :- member2(D,Z).

% ------------- domain knowledge -------------

digit(N) :- N in 0..9.

member2(D,Z) :- digit(D), at(D,1), Z #= 1.
member2(D,Z) :- digit(D), at(D,2), Z #= 1.
member2(D,Z) :- digit(D), at(D,3), Z #= 1.

member2(D,Z) :- digit(D1), at(D1,1),
		digit(D2), at(D2,2),
		digit(D3), at(D3,3),
		D1 #\= D,
		D2 #\= D,
		D3 #\= D,
		Z #= 0.
	

% --------------------------------------------



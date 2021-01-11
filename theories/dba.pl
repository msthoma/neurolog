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
label([R]) :- dba(R).

% ------------- domain knowledge -------------

symbol(0).
symbol(1).
symbol(2).
symbol(3).

dba(1) :-
   symbol(D1), at(D1,1),
   symbol(D2), at(D2,2),
   symbol(D3), at(D3,3),
   symbol(D4), at(D4,4),
   symbol(D5), at(D5,5),
   isvalid(D1, D2, D3, D4, D5).

dba(0) :-
   symbol(D1), at(D1,1),
   symbol(D2), at(D2,2),
   symbol(D3), at(D3,3),
   symbol(D4), at(D4,4),
   symbol(D5), at(D5,5),
   \+ isvalid(D1, D2, D3, D4, D5).

isvalid(D1, 2, D2, 3, D3) :- D3 is D1+D2.  
isvalid(D1, 3, D2, 2, D3) :- D1 is D2+D3. 

% --------------------------------------------



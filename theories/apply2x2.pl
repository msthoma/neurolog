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

label([D1, D2 ,D3, R1, R2, C1, C2]) :- apply2x2(D1, D2 ,D3, R1, R2, C1, C2).

% ------------- domain knowledge -------------

op(N) :- N in 1..3.

apply2x2(D1, D2 ,D3, R1, R2, C1, C2) :-
   op(O1), at(O1,1),
   op(O2), at(O2,2),
   op(O3), at(O3,3),
   op(O4), at(O4,4),
   aux(D1,O1,D2,O2,D3,R1),	
   aux(D1,O3,D2,O4,D3,R2),	
   aux(D1,O1,D2,O3,D3,C1),	  
   aux(D1,O2,D2,O4,D3,C2).	

aux(D1,1,D2,1,D3, Z) :- Z #= (D1 + D2) + D3.
aux(D1,2,D2,2,D3, Z) :- Z #= (D1 - D2) - D3.
aux(D1,3,D2,3,D3, Z) :- Z #= (D1 * D2) * D3.
aux(D1,1,D2,2,D3, Z) :- Z #= (D1 + D2) - D3.       
aux(D1,2,D2,1,D3, Z) :- Z #= (D1 - D2) + D3.  
aux(D1,1,D2,3,D3, Z) :- Z #= (D1 + D2) * D3.        
aux(D1,3,D2,1,D3, Z) :- Z #= (D1 * D2) + D3.  
aux(D1,2,D2,3,D3, Z) :- Z #= (D1 - D2) * D3.        
aux(D1,3,D2,2,D3, Z) :- Z #= (D1 * D2) - D3.   

% --------------------------------------------



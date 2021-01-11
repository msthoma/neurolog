% ---------------- Chess ----------------
% ++++++++++++++++++++++++++++++++++++++++++++

:- use_module(library(clpfd)).
:- use_module(library(between)).
:- use_module(library(lists)).

:- go.

% --------------------------------------------

go :-
   write('\n\npreparing query...\n'),
   load_theory('SICSTUS_BIN/chess.pl'), nl,
   enforce_labeling(true), nl,
%   spy abduction:rule,
   load_scenario(Sc,Label,ID),
   write('\n\nexecuting query...\n'),
   write(scenario(Sc,Label,ID)), nl, nl,
   tellfile('SICSTUS_BIN/outputs/',ID,'.txt'),
   write(scenario(Sc,Label,ID)), nl,
   query_all([label(Label)]),
   told,
   fail.
go :- halt.

% --------------------------------------------

size(3).
pieces([b(k),w(k),w(q),w(r),w(b),w(n),w(p)]). % all w() 6160
%pieces([b(k),w(k),w(r),w(b),w(n),w(p)]). % no w(q) 3920
%pieces([b(k),w(k),w(r),w(b),w(n)]). % no w(q) no w(p)
%pieces([b(k),w(k),w(q)]). % mini version
dist(D) :- size(S), between(1,S,D). % should not start from 0
piece(P) :- pieces(Ps), member(P,Ps).
pos((X,Y)) :- size(S), between(1,S,X), between(1,S,Y).

:- dynamic input_constr/1.
load_scenario(Sc,Label,ID) :-
   ['SICSTUS_BIN/input.pl'],
   input(scenario(Sc,Label,ID),Constr),
   retractall(input_constr(_)),
   assert(input_constr(Constr)).
in_pieces(ATs) :-
   input_constr(ATs).
in_empties(EMs) :-
   input_constr(ATs),
   findall(empty(Z), (
      pos(Z), \+member(at(_,Z),ATs)
   ), EMs).

perturb(Conf,Cost) :-
   input_constr(Constr),
   findall((Cost,(PZ,Ws)), (
      piece(w(P1)), piece(w(P2)), P1\=P2,
      pos(PZ1), pos(PZ2), PZ1\=PZ2,
      piece(b(k)), pos(PZ), PZ\=PZ1, PZ\=PZ2,
      \+ kings_close(PZ,P1,PZ1),
      \+ kings_close(PZ,P2,PZ2),
      sort([(PZ1,w(P1)),(PZ2,w(P2))],Ws),
      Placed=[at(b(k),PZ),at(w(P1),PZ1),at(w(P2),PZ2)],
      penalize(Constr,Placed,Cost)
   ), AllCostConf),
   sort(AllCostConf,SortCostConf),
   %SortCostConf = [(MinCost,_)|_],
   %member((MinCost,Conf),SortCostConf).
   member((Cost,Conf),SortCostConf).

kings_close((BX,BY),k,(WX,WY)) :-
   eval(BX,WX,abs,DX), 1 >= DX,
   eval(BY,WY,abd,DY), 1 >= DY,
   eval(DX,DY,sum,S), 0 < S.

penalize(Constr,Conf,Cost) :-
   count((
      member(hard(AT),Constr),
      \+member(AT,Conf)
   ), C1),
   C1=0, % prune out violations
   count((
      member(soft(at(_,Z)),Constr),
      \+member(at(_,Z),Conf)
   ), C2),
   count((
      member(at(_,Z),Conf),
      \+member(soft(at(_,Z)),Constr)
   ), C3),
   count((
      member(soft(at(P1,Z)),Constr),
      member(at(P2,Z),Conf), P1\=P2
   ), C4),
   Cost is C1*100 + C2*10 + C3*10 + C4.

count(Cond,Num) :-
   findall([], call(Cond), All), length(All,Num).

eval(A,B,abs,C) :- C is abs(A-B).
eval(A,B,sum,C) :- C is A+B.
eval(A,B,min,C) :- C is min(A,B).

% --------------------------------------------

show(X) :- write(X), nl, flush_output.

:- dynamic tracktab/1.
tracktab(0).

track(Q-in,X) :- tracktab(N), spacing(N), show(Q-in-X), track(in).
track(Q-out,X) :- track(out), tracktab(N), spacing(N), show(Q-out-X).
track(Q-out,X) :- track(in). % on backtrack
track(Q,X) :- Q\=_-in, Q\=_-out, tracktab(N), spacing(N), show(Q-X).

track(in) :-
   retractall(tracktab(N)),
   N1 is N+1,
   assert(tracktab(N1)).

track(out) :-
   retractall(tracktab(N)),
   N1 is N-1,
   assert(tracktab(N1)).

spacing(0) :- !.
spacing(N) :- N1 is N-1, spacing(N1), write(' ').

:- dynamic counter/1.
counter(0).
count(reset) :- retractall(counter(_)), assert(counter(0)).
countup(N1) :- retractall(counter(N)), N1 is N+1, assert(counter(N1)).

tellfile(Path,Varname,Ext) :-
   number_chars(Varname,Cs), atom_chars(Str,Cs),
   atom_concat(Str,Ext,Filename),
   atom_concat(Path,Filename,FullFilename),
   tell(FullFilename).

:- dynamic switched/2.
switch(N,get,V) :- switched(N,V).
switch(N,set,V) :- retractall(switched(N,_)), assert(switched(N,V)).

% --------------------------------------------

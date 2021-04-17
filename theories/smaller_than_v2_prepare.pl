% ---------------- Basic Dom -----------------
% ++++++++++++++++++++++++++++++++++++++++++++

:- use_module(library(clpfd)).
:- use_module(library(between)).
:- use_module(library(lists)).

:- go.

% --------------------------------------------

go :-
   write('\n\npreparing query...\n'),
   load_theory('SICSTUS_BIN/smaller_than.pl'), nl,
   enforce_labeling(true), nl,
   load_instance(ID,Label),
   write('\n\nexecuting query...\n'),
   write(instance(ID,Label)), nl, nl,
   tellfile('SICSTUS_BIN/proofs/',ID,'.txt'),
   write(instance(ID,Label)), nl,
   query_all([label(Label)]),
   told,
   fail.
go :- halt.

% --------------------------------------------

:- dynamic sidefeed/1.
load_instance(ID,Label) :-
   ['SICSTUS_BIN/smaller_than_instance.pl'],
   instance(ID,Label,SF),
   retractall(sidefeed(_)),
   assert(sidefeed(SF)).

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

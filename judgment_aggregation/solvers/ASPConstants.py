BASIC_JA_ASP = """\
% generate literals over all issues
ilit(X) :- issue(X).
ilit(-X) :- issue(X).
lit(X) :- ilit(X).
% generate literals over all auxiliary variables
lit(X) :- aux(X).
lit(-X) :- aux(X).
% auxiliary predicate for variables
var(X) :- issue(X).
var(X) :- aux(X).

% auxiliary predicates for counting/identifying issues, literals, voters
numissues(N) :- N = #count { Z : issue(Z) }.
issuenum(1..N) :- numissues(N).

numilits(N) :- N = #count { Z : ilit(Z) }.
ilitnum(1..N) :- numilits(N).

numlits(N) :- N = #count { Z : lit(Z) }.
litnum(1..N) :- numlits(N).

numvars(N) :- N = #count { Z : var(Z) }.
varnum(1..N) :- numvars(N).

numvoters(N) :- N = #count { A : voter(A) }.
voternum(1..N) :- numvoters(N).

% auxiliary predicate for finding clauses
clause(C) :- clause(C,_).

% every voter is an agent
agent(A) :- voter(A).

% require that every agent has a judgment set
% + completeness (& negation-freeness)
1 { js(A,X); js(A,-X) } 1 :- agent(A), lit(X).

% constraint consistency (CNF)
:- agent(A), clause(C), js(A,-L) : clause(C,L).

% generate a collective outcome
agent(col).
% auxiliary predicate to refer to the collective outcome
collective(X) :- js(col,X), ilit(X).

% show only the collective outcome
#show collective/1.
"""

ASP_PROCEDURES = {
    "kemeny":
    """\
% determine support for each issue literal
pc(X,N) :- ilit(X), N = #count { A : voter(A), js(A,X) }.

% use the technique of saturation (see Eiter & Gottlob '95)
w :- not w.
virtual(X) :- ilit(X), w.
% guess a virtual assignment
virtual(X) ; virtual(-X) :- var(X).
% remove virtual assignments that are contradictory
w :- var(X), virtual(X), virtual(-X).
% remove virtual assignments that don't satisfy integrity constraint
w :- clause(C), virtual(-L) : clause(C,L).

% order the variables alphabetically
1 { varorder(X,O) : varnum(O) } 1 :- var(X).
1 { varorder(X,O) : var(X) } 1 :- varnum(O).
:- varorder(X1,O1), varorder(X2,O2), X1 < X2, O1 > O2.

% order the voters alphabetically
1 { voterorder(A,O) : voternum(O) } 1 :- voter(A).
1 { voterorder(A,O) : voter(A) } 1 :- voternum(O).
:- voterorder(A1,O1), voterorder(A2,O2), A1 < A2, O1 > O2.

% compute the distance from the virtual assignment to the profile
% virtdist(Var,Voter,Ans)
virtdist(0,N,0) :- numvoters(N).
virtdist(Xn,An,C) :-
  varnum(Xn), varorder(X,Xn),
  voternum(An), voterorder(A,An),
  virtdist(Xn,An-1,C), virtual(X), js(A,X).
virtdist(Xn,An,C) :-
  varnum(Xn), varorder(X,Xn),
  voternum(An), voterorder(A,An),
  virtdist(Xn,An-1,D), C = D+1, virtual(X), js(A,-X).
virtdist(Xn,An,C) :-
  varnum(Xn), varorder(X,Xn),
  voternum(An), voterorder(A,An),
  virtdist(Xn,An-1,C), virtual(-X), js(A,-X).
virtdist(Xn,An,C) :-
  varnum(Xn), varorder(X,Xn),
  voternum(An), voterorder(A,An),
  virtdist(Xn,An-1,D), C = D+1, virtual(-X), js(A,X).
virtdist(Xn,0,C) :- varnum(Xn), numvoters(N), virtdist(Xn-1,N,C).
virtdist(D) :- virtdist(M,N,D), numvars(M), numvoters(N).
% saturate all virtdist/3 in case w is derived
%virtdist(0..M,0..N,0..C) :- w, numvars(M), numvoters(N), C = N*M.
virtdist(Xn,An,0..C) :- w, varnum(Xn), voternum(An), numvars(M), C = M*Xn.

% compute the distance from the collective assignment to the profile
coldist(D) :- D = #sum { N,pc(X,N) : js(col,-X), pc(X,N) }.

% remove virtual assignments that have distance at least that of the
% collective outcome
w :- virtdist(D1), coldist(D2), D1 >= D2.""",
    "kemeny-opt1":
    """\
% determine the Hamming distance from each voter's judgment set to the outcome
dist(A,D) :- voter(A), D = #count { X : ilit(X), js(col,X), js(A,-X) }.

% sum the distances over all voters
dist(E) :- E = #sum { D,dist(A,D) : dist(A,D) }.

% minimize the cumulative distance
#minimize { E@10,dist(E) : dist(E) }.""",
    "kemeny-opt2":
    """\
% determine score for each voter A and each issue literal X
% (1 if A has X in their judgment set; 0 otherwise)
score(A,X,D) :- voter(A), ilit(X), D=1, js(A,X), js(col,X).
% sum scores over all agents and all literals
score(E) :- E = #sum { D,score(A,X,D) : score(A,X,D) }.
% maximize the total score
#maximize { E@10,score(E) : score(E) }.""",
    "kemeny-opt3":
    """\
% determine the Hamming distance from each voter's judgment set to the outcome
dist(A,D) :- voter(A), D = #count { X : ilit(X), js(col,X), js(A,-X) }.
% sum the distances over all voters
dist(E) :- E = #sum { D,dist(A,D) : dist(A,D) }.
% minimize the cumulative distance
#minimize { E@10,dist(E) : dist(E) }.""",
    "slater":
    """\
% determine the majority outcome
pc(X,N) :- ilit(X), N = #count { A : voter(A), js(A,X) }.
maj(X) :- ilit(X), pc(X,N), pc(-X,M), N > M.
% maximize agreement with the majority outcome
#minimize { 1@10,maj(X) : maj(X), js(col,-X) }."""
}

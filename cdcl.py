import numpy as np  # using np.array is more computationally efficient when there is no expansion
from dataclasses import dataclass   # class now is like struct in C++ (simpler and just for data grouping)

@dataclass(frozen=True)
class Literal:
    """
        a literal in a clause, including the variable (as an int) and its negation status (True | False)
    """
    variable: int
    negation: bool  # to mark whether a literal is negated
    # def __init__(self, literal: int) -> None:
    #     self.variable = abs(literal)
    #     self.negation = (literal < 0)

class Clause:
    literals: np.array # all literals of the clause
    def __init__(self, literals: list[Literal]) -> None:
        self.literals = np.array(literals)
    
    def __iter__(self):
        """
            iterate a clause is to iterate its list of literals
        """
        return iter(self.literals) 
    
    def status(self, assignments):
        """
            input: dict of all assignments
            returns:
                - status of a clause, which is 1 of the following: 'satisfied', 'unsatisfied' (which is conflict), 'unit', 'unresolved'
                - num:
                    - if 'satisfied' or 'unsatisfied' or 'unresolved': num = None
                    - if 'unit': num = index of the unassigned literal in the clause

        """
        # list of values corresponds to list of literals in the clause
        values = []
        unassigned_idx = None
        for id in range( len(self.literals) ):
            lit = self.literals[id]
            if not assignments.check_existence(lit.variable):
                values.append(None)
                if unassigned_idx == None:
                    unassigned_idx = id
                else:
                    unassigned_idx = False
            else:
                if lit.negation:
                    val = not assignments[lit.variable]
                    values.append( val )
                else:
                    val = assignments[lit.variable]
                    values.append( val )
                
                if val == True:
                    return 'satisfied', None

        # there is no True in `values`

        cnt = values.count(False)
        if cnt == len(values):
            # all are False
            return 'unsatisfied', None
        
        if cnt == len(values) - 1:
            # one is unassigned, others are False
            return 'unit', unassigned_idx
        
        # neither of the above
        return 'unresolved', None
        
    def __getitem__(self, id: int) -> Literal:
        """
            get the Literal at index `id` in list of Clauses
            input: `id` NON-NEGATIVE number and must be in range(len(self.literals))
        """
        if id > len(self.literals) or id < 0:
            raise IndexError('Clause::__getitem__: index out of range.')
        
        return self.literals[id]

class CNF:
    """
        a CNF formula, including clauses and list of variables (for later use) 
    """
    clauses: list           # an array of Clause objects
    variables: np.array     # an array of variables as ints

    def __init__(self, clauses: list, variables: list) -> None:
        """
            - input:
                - list of clauses in the format as the following example: clauses = [[-1,2,3], [-1,3,-5], [-5]]
                - list of UNIQUE variable (unsigned). In the above example, variables = [1,2,3,5]
        """
        # construct list of object Clause, each of which is a list of object Literal
        self.clauses = []    # list of object Clause
        for clause in clauses:
            _ = []  # list of object Literal
            for lit in clause:
                _.append(
                    Literal(
                        variable=abs(lit),
                        negation=(lit < 0)
                    )
                )
            self.clauses.append(
                Clause(literals=_)
            )

        self.variables = np.array(variables)

    def __iter__(self):
        # iterating an CNF formula is iterating its list of Clauses
        return iter(self.clauses)

class Assignment:
    variable: int
    value: bool
    antecedent: Clause
    decision_level: int
    def __init__(self, variable: int, value: bool, antecedent: Clause, decision_level: int) -> None:
        self.variable = variable
        self.value = value
        self.antecedent = antecedent
        self.decision_level = decision_level

class Assignments(dict):
    """
        contains all current partial assignments as a map:
            - key: variable
            - value: Assignment object
    """
    def __init__(self) -> None:
        super().__init__()

    def assign(self, variable: int, value: bool, antecedent: Clause, dl: int):
        self[variable] = Assignment(
            variable=variable,
            value=value,
            antecedent=antecedent,
            decision_level=dl
        )

    def unassign(self, variable: int):
        try:
            self.pop( variable )
        except: # do nothing
            pass
    
    def __getitem__(self, variable: int) -> Assignment:
        """
            allow caller to user [] operator to access assignment with variable without any errors even it does not exist in the dict
        """
        return self.get(variable)
        

    def check_existence(self, variable: int):
        """
            check whether the variable had already been assigned in the assignment list
        """
        return bool(self.get(variable))

class CDCL:
    _current_dl = 0     # keep current decision level when processing

    @staticmethod
    def __resolution_operation(
        this: Clause,
        that: Clause,
        var: int
    ):
        """
            apply resolution operation on 2 clause and returns the resulted clause
        """
        res = set(np.append(this.literals, that.literals)) - { Literal(var, True), Literal(var, False) }
        return Clause( literals=list(res) )

    @staticmethod
    def __unit_propagation(
        cnf: CNF,
        assignments: Assignments
    ):
        """
            do unit propagation until there is no unit clause or a conflict occurs
            returns:
                - status: str, 1 of the following:
                    - 'conflict' if any clause is currently unsatisfied within the given assignments
                    - 'unresolved' if no conflict occurs
                - clause: if conflicts, returns the conflict clause; otherwise, returns None
        """
        finished = False
        while not finished:
            # keep going until no unit clause remains
            finished = True
            for clause in cnf:
                status, id = clause.status(assignments=assignments)
                if status == 'unit': # is unit clause
                    # get the unassigned variables in the unit clause
                    unassigned_literal = clause[id]
                    var = unassigned_literal.variable
                    val = not unassigned_literal.negation

                    assignments.assign(
                        variable=var,
                        value=val,
                        antecedent=clause,
                        dl=CDCL._current_dl
                    )
                    finished = False # continue
                elif status == 'unsatisfied':
                    # conflict
                    return ('conflict', clause)
                else:
                    continue
        return ('unresolved', None)
    
    @staticmethod
    def __check_all_variables_assigned(
        cnf: CNF,
        assignments: Assignments
    ): 
        return len(assignments) == len(cnf.variables)

    @staticmethod
    def __pick_branching_variable(
        cnf: CNF,
        assignments: Assignments
    ):
        pass

    @staticmethod
    def __conflict_analysis(
        conflict_clause: Clause,
        assignments: Assignments
    ):
        """
            When a conflict occurs due to unit propagation, we invoke conflict analysis to choose a decision level to go back, instead of normally backtracking. This process differs CDCL from DPLL.

            Conflict analysis following the formula given in this site: https://kienyew.github.io/CDCL-SAT-Solver-from-Scratch/The-Theory.html#exploiting-structure-with-uips

            returns (b, clause):
                - b: decision level to go back when do backtracking
                - clause: the new learnt clause to be added to the KB (cnf)  
        """
        # call it "clause" in general; this is the intermediate clause when processing
        clause = conflict_clause

        # get literals assigned at current decision level and must have antecedent (as intermediate clause will be resolved with antecedents)
        literals = [lit for lit in clause if assignments[lit.variable].dl == CDCL._current_dl and assignments[lit.variable].antecedent != None]


        # constantly resolve each lit in literals with the latest intermediate clause in the list
        # NOTE: new intermediate literals can be added to the above literal list.
        while len(literals) != 1:
            # len > 1 or len == 0: the last len is the new learnt clause || len == 0 means empty clause
            lit = literals[0]
            antecedent = assignments[lit.variable].antecedent

            # w(n) = w(n-1) resolve (antecedent of lit)
            clause = CDCL.__resolution_operation(clause, antecedent, lit.variable)
            
            # as `clause` may have changed so that we need to reconstruct list of literals
            literals = [lit for lit in clause if assignments[lit.variable].dl == CDCL._current_dl and assignments[lit.variable].antecedent != None]
        
        # after all, `clause` is the latest intermediate clause, which is the new learnt clause
        # compute backtrack level:
        # - the deepest assignment level of literals in the clause is current 
        decision_levels = sorted( set(assignments[lit.variable].dl for lit in clause) )
    
    @staticmethod
    def __backtrack(
        cnf: CNF,
        assignments: Assignments,
        kept_dl: int    # dl to go back to after backtracking
    ):
        """
        
        """

    @staticmethod
    def __CDCL(cnf: CNF, assignments: Assignments):
        """
            run CDCL algorithm to solve the given CNF formula
            input: cnf formula as np.array, a dict `assignments` that will contain all assignments
            returns the result as a list of literals (e.g., [-1,2,-3,-4]) if exists; otherwise, returns None
        """
        status, clause = CDCL.__unit_propagation(
            cnf=cnf,
            assignments=assignments
        )
        if status == "conflict":
            return None

        CDCL._current_dl = 0    # decision level: current depth
        while not CDCL.__check_all_variables_assigned(cnf=cnf,assignments=assignments):
            var, val = CDCL.__pick_branching_variable(
                cnf=cnf,
                assignments=assignments
            )

            CDCL._current_dl += 1

            assignments.assign(
                variable=var,
                value=val,
                antecedent=None,
                dl=CDCL._current_dl
            )

            status, clause = CDCL.__unit_propagation(
                cnf=cnf,
                assignments=assignments
            )

            if status != 'conflict':
                # if unit propagation does not lead to conflict, there is nothing to do
                break
            
            # a conflict occurs with current set of assignments
            # analyse the conflict
            b = CDCL.__conflict_analysis(
                conflict_clause=clause,
                assignments=assignments
            )

            if b < 0:
                return False
            else:
                CDCL.__backtrack(
                    cnf=cnf,
                    assignments=assignments,
                    kept_dl=b
                )
                CDCL._current_dl = b
        return True

    @staticmethod
    def solve(cnf: CNF):
        assignments = Assignments()
        cdcl = CDCL.__CDCL(cnf=cnf, assignments=assignments)

class Solver:
    __cnf: CNF  # the CNF formula to be solved
    def __init__(self, clauses: list[list[int]], variables: list[int]) -> None:
        self.__cnf = CNF( clauses=clauses, variables=variables )

    def solve(self):
        return CDCL.solve(self.__cnf)
    
if __name__ == "__main__":
    sol = Solver([[-1,2,3], [-1,3,-5], [-5]], [1,2,3,5])
    sol.solve()
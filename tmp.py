import numpy as np  # using np.array is more computationally efficient when there is no expansion
from dataclasses import dataclass   # class now is like struct in C++ (simpler and just for data grouping)

@dataclass(frozen=True)
class Assignment:
    """
        - represents an assignment
        - each instance maps a variable to one of 2 boolean values: True | False
        - all created assigment
    """
    variable: int               # an integer represents a variable
    value: bool                 # boolean value of the variable True | False
    antecedent: np.array[int]   # a clause as an array
    dl: int                     # decision level in which the assigment occurs

class Assignments(dict):
    """
        a dictionary that keeps all Assignment instances
    """
    def __init__(self) -> None:
        super().__init__()
    
    def assign(self, variable: int, value: bool, antecedent: Clause, dl: int) -> None:
        """
            add a new assignment to the list of assigments using variable as key
        """
        
        self[ object.variable ] = Assignment(
            variable=variable,
            value=value,
            antecedent=antecedent,
            dl=dl
        )

    def unassign(self, variable: int) -> None:
        """
            unassign a variable
        """
        try:
            self.pop( variable )
        except: # do nothing
            pass
    
    def __getitem__(self, variable: int) -> bool | None:
        """
            get the boolean value corresponding to the given variable

            returns the value if exists; otherwise, returns None
        """
        tmp = self.get( variable )
        if tmp == None:
            return None
        return tmp.value

@dataclass(frozen=True)
class Literal:
    """
        a literal in a clause, including the variable (as an int) and its negation status (True | False)
    """
    variable: int
    negation: bool  # to mark whether a literal is negated

class Clause:
    literals: np.array[Literal] # all literals of the clause
    def __init__(self, literals: np.array[Literal]) -> None:
        self.literals = literals

    def __iter__(self):
        """
            iterate a clause is to iterate its list of literals
        """
        return iter(self.literals)
    
    def status(self, assignments: Assignments) -> str['unit' | 'satisfied' | 'unsatisfied' | 'resolved']:
        """
            return 1 of 4 status of a clause: 'unit', 'satisfied', 'unsatisfied', 'unresolved'
        """
        values = [] # assign status of each literal in the clause at the same index to the literal in the array self.literals
        for literal in self.literals:
            literal: Literal
            val = assignments[ literal.variable ]
            if val == None:
                # unassigned
                values.append(None)
            elif val == True:
                return 'satisfied'
            else:
                values.append(val)
        # there is NO True in 'values'

        cnt = values.count( False )
        if cnt == len(values):
            return 'unsatisfied'
        
        if cnt == len(values) - 1:
            # one is unassigned, others are assigned 0
            return 'unit'

        # neither of the above:
        return 'unresolved'



class CNF:
    """
        a CNF formula, including clauses and list of variables (for later use) 
    """
    clauses: np.array[Clause]   # all the clause of the CNF formula
    variables: np.array[int]    # all variables in the CNF formula
    def __init__(self, clauses: list[list]) -> None:
        # get set of clauses
        self.clauses = np.array( [np.array(clause) for clause in clauses] )
        
        # get set of variables
        tmp_vars = {}
        variables = []
        for clause in self.clauses:
            for lit in clause:
                if tmp_vars.get( lit.variable ) == None:
                    variables.append(lit.variable)
        self.variables = np.array(variables)


class CDCL:
    """
        - An implementation of CDCL algorithm, including ***STATIC METHODS***.
        - Albeit creating CDCL instances raises no error, you should not do so as it is meaningless.
    """
    __assignment = {} # a list that map a variable to its corresponding assignment object
    # @staticmethod
    # def __search_restart():
    #     """

    #     """
    
    # @staticmethod
    # def __clause_deletion():
    #     """

    #     """
    
    @staticmethod
    def resoltion_operator(this: Clause, that: Clause, var: int):
        """
            resolution operator: to resolve 2 clause - union them and remove 2 conflict literals
            returns the resulted clause
        """
        res = set(this.literals + that.literals) - {Literal(variable=var, negation=True), Literal(variable=var, negation=False)}
        return Clause( np.array(res) )
    
    @staticmethod
    def __check_all_variables_assigned() -> True | False:
        """
            to test if all variables in a CNF have been assigned
            return True
        """

    @staticmethod
    def __unit_propagation(cnf: np.array[np.array], assignments: Assignments):
        """
            do unit propagation on the cnf formula with current assignments list 
        """
        finish = 

    @staticmethod
    def __pick_branching_variable(cnf: np.array[np.array], assignments: Assignments):
        """
            to select a variable to assign a value

            heuristic: ................................
        """
        unassigned_vars = 

    @staticmethod
    def __conflict_analysis(cnf: np.array[np.array], assignments: Assignments):
        """
        
        """

    @staticmethod
    def __backtrack(cnf: np.array[np.array], assignments: Assignments, kept_dl: int):
        """
        
        """

    @staticmethod
    def __CDCL(cnf: np.array[np.array], assignments: Assignments):
        """
            run CDCL algorithm to solve the given CNF formula
            input: cnf formula as np.array, a dict `assignments` that will contain all assignments
            returns the result if exists; otherwise, returns None
        """
        unit_prop = CDCL.__unit_propagation(
            cnf=cnf,
            assignments=assignments
        )
        if unit_prop == "conflict":
            return None

        dl = 0 # decision level: current depth
        while not CDCL.__check_all_variables_assigned(cnf=cnf,assignments=assignments):
            var, val = CDCL.__pick_branching_variable(
                cnf=cnf,
                assignments=assignments
            )
            dl += 1
            assignments.assign(
                variable=var,
                value=val,
                antecedent=None,
                dl = dl
            )

            unit_prop = CDCL.__unit_propagation(
                cnf=cnf,
                assignments=assignments
            )

            if unit_prop == "conflict":
                break
            b = CDCL.__conflict_analysis(
                cnf=cnf,
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
                dl = b
        return True

    @staticmethod
    def solver(cnf: list[list]):
        """
            input: cnf as a list of clauses, each of which is a list of literals represented by an integer
            returns the result if exists; otherwise, returns None
        """
        # convert typical Python list to a numpy array
        cnf = CNF( clauses=cnf )

        # initialize a list of partial assignments
        assignments = Assignments() # get the list of all assignments in the solver

        return CDCL.__CDCL(cnf=cnf, assignments=assignments)
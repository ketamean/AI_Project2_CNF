import numpy as np  # using np.array is more efficient
from dataclasses import dataclass   # class now is like struct in C++ (simpler and just for data grouping)

@dataclass
class Literal:
    """
        a literal in a clause, including the variable (as an int) and its negation status (True | False)
    """
    variable: int
    negation: bool  # to mark whether a literal is negated

@dataclass
class Clause:
    literals: np.array[Literal] # all literals of the clause

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

@dataclass
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
        self.dl = 0
    
    def assign(self, variable: int, value: bool, antecedent: Clause):
        """
            add a new assignment to the list of assigments using variable as key
        """
        
        self[ object.variable ] = Assignment(
            variable=variable,
            value=value,
            antecedent=antecedent,
            dl=self.dl
        )

    def unassign(self, variable: int):
        try:
            self.pop( variable )
        except: # do nothing
            pass
    
    def __getitem__(self, key: int):
        """
        
        """
        # return super().__getitem__(key)


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
    def __check_all_variables_assigned() -> True | False:
        """
            to test if all variables in a CNF have been assigned
            return True
        """

    @staticmethod
    def __unit_propagation(cnf: np.array[np.array], assignments: Assignments):
        """

        """

    @staticmethod
    def __pick__branching_variable(cnf: np.array[np.array], assignments: Assignments):
        """
            to select a variable to assign a value

            heuristic: ................................
        """
        unassigned_vars = #np.array([var for var in cnf.variables if assignments.get(var) == None])

    @staticmethod
    def __conflict_analysis(cnf: np.array[np.array], assignments: Assignments):
        """
        
        """

    @staticmethod
    def __backtrack(cnf: np.array[np.array], assignments: Assignments, kept_dl: int):
        """
        
        """

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
        unit_prop = CDCL.__unit_propagation(
            cnf=cnf,
            assignments=assignments
        )
        if unit_prop == "conflict":
            return None

        dl = 0 # decision level: current depth
        while not CDCL.__check_all_variables_assigned(cnf=cnf,assignments=assignments):
            var, val = CDCL.__pick__branching_variable(
                cnf=cnf,
                assignments=assignments
            )
            dl += 1
            assignments.dl = dl
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

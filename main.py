# import cdcl
import Brute_force_solver
import PySAT

def main(filepath):
    # Simple CLI
    print("Choose the method to solve the problem:")
    # print("1. CDCL")
    print("2. PySAT")
    print("3. Brute Force")
    choice = input("Enter your choice: ")
    #if choice == "1":
    #    print("CDCL")
    #    cnf = []
    #    print(cdcl.CDCL.solver(cnf))  # should return True | False | None
    if choice == "2":
        print("PySAT")
        gem_hunter = PySAT.GemHunter()
        gem_hunter.gen_board(filepath)
        solver = input("Enter the solver name (g4, g3, m22, etc): ")
        result = gem_hunter.solve(solver) # Others: 'g4', Cadical(), etc.
        if result:
            print('\nSolution:')
            for row in result:
                print(','.join(row))
        else:
            print('No solution found.')
    elif choice == "3":
        print("Brute Force")
        brute_force_gem_hunter = Brute_force_solver.BruteForceGemHunter()
        brute_force_gem_hunter.gen_board(filepath)
        brute_force_gem_hunter.brute_force_solve()
    else:
        print("Invalid choice. Please try again.")
        
        
if __name__ == '__main__':
    print("-----------Welcome to Gem Hunter!-----------")
    filepath = input("Enter the path of the input file (.txt): ")
    main(filepath)
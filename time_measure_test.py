from main import GemHunter
import time
import matplotlib.pyplot as plt

FILEPATH = 'testcases/test5.txt'

"""
    all type of solving will be run on the same map.
    the final time measurement is average of N runs. You can define N below
"""
N_runs = 3

if __name__ == '__main__':
    game = GemHunter()
    game.gen_board(FILEPATH)
    total_avg = [] # average time for each solving method (numbered as in the dict below)
    run = {
        1: "PySAT", 
        # FOR THIS TO WORK PROPERLY, YOU NEED TO GO TO main.py AND UNCOMMENT THE LINE 52 (solver_name = input('Please enter the name of a PySAT solver (g4, g3, m22, etc): ')
        # AND CHANGE THE LINE 53 TO pysat_solver = PySAT.PySatSolver(clauses, solver_name)
        2: "CDCL (self implementation)",
        3: "Backtracking algorithm",
        4: "Brute-force algorithm",
    }

    for type, name in run.items():
        durations = []
        for _ in range(N_runs):
            start = time.time()
            game.solve(type, FILEPATH)
            end = time.time()
            durations.append( end - start )
        avg = 0
        for d in durations:
            avg += d
        avg /= len(durations)

        print(f'{name}: {avg} second')
        total_avg.append(avg)
        print('-----------------')
        
        
    # line graph
    for v in total_avg:
        plt.plot(run.values(), total_avg, marker='o', color = 'b')
    plt.ylabel('Time (s)')
    plt.xlabel('Solving method')
    plt.title('Time measurement for solving methods')
    
    plt.show()



    

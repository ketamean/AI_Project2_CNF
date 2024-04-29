from main import GemHunter
import time
FILEPATH = 'testcases/test3.txt'

"""
    all type of solving will be run on the same map.
    the final time measurement is average of N runs. You can define N below
"""
N_runs = 3

if __name__ == '__main__':
    game = GemHunter()
    game.gen_board(FILEPATH)
    run = {
        1: "PySAT",
        2: "CDCL (self implementation)",
        3: "Backtracking algorithm",
        #4: "Brute-force algorithm",
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
        print('-----------------')
    
    
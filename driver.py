from game import Watersort
from heapq import heappop, heappush
from collections import deque
from termcolor import colored
from time import time
import tracemalloc as tm

# Some functions
def check(tube_set:list):
        return all((len(tube) == game.capacity or len(tube) == 0) and len(set(tube)) <= 1 for tube in tube_set)
        
def countCombinedTop(tube:list):
        col_count = 1
        for index in range(-2, -len(tube)-1, -1):
            if tube[index] == tube[-1]:
                col_count += 1
            else: break
        return col_count

def getValidMoves(tube_set:list):
        moves = []
        for i, source in enumerate(tube_set):
            if not source: continue
                
            for j, target in enumerate(tube_set):
                    
                col_count = countCombinedTop(source)
                if i == j or (target and (target[-1] != source[-1] or len(target) + col_count > game.capacity)):
                    continue
                moves.append((i+1, j+1))
                
        return moves

# Time: O(b^d) | Space: O(d * n * h)
# b = number of valid moves on each state
# d = number of moves required
# n = number of tubes
# h = tube height (capacity)
def backtrack_solve(game:Watersort, current_state=[],  path=[]):
    tubes = game.tubeset.copy()
    if check(tubes):
        return path

    for i, j in getValidMoves(tubes):
        # Make the move
        new_tubes = [list(tube) for tube in tubes]
        new_tubes[j-1].append(new_tubes[i-1].pop())
        result = backtrack_solve(game, new_tubes, path + [(i, j)])
        if result:  # If a solution is found
            return result
    return None  # Backtrack if no moves lead to a solution
    
# Time: O(b^d) with fewer states given a good heuristic | Space: O(b^d * n * h)
# b = number of valid moves on each state
# d = number of moves required
# n = number of tubes
# h = tube height (capacity)
def a_star_solve(game:Watersort):
    def heuristic(tubes):
        return sum(1 for tube in tubes if (len(set(tube)) > 1 or (len(tube) != 4 or len(tube) != 0)))
    
    tubes           = game.tubeset.copy()
    initial_state   = tuple(tuple(tube) for tube in tubes)
    pq              = [(heuristic(tubes), 0, initial_state, [])]  # (priority, moves, state, path)
    visited         = set()

    while pq:
        # Extract pop data
        _, moves, current_state, path = heappop(pq)
        
        # Skip if current state has already been visited
        if current_state not in visited: visited.add(current_state)

        # Check if current state is the solution state
        if check(current_state): return path

        # Explore valid moves from current state and add them to the priority queue with updated priority and moves count
        for i, j in getValidMoves(current_state):
            # Make the move
            new_state = [list(tube) for tube in current_state]
            
            for _ in range(countCombinedTop(new_state[i-1])):
                new_state[j-1].append(new_state[i-1].pop())
            
            new_state = tuple(tuple(tube) for tube in new_state)

            if new_state not in visited:
                heappush(pq, (moves + 1 + heuristic(new_state), moves + 1, new_state, path + [(i, j)]))

    return None  # No solution found

# Time: O(b^d) | Space: O(d)
# b = number of valid moves on each state
# d = number of moves required
def dfs_solve(game:Watersort):
    tubes = game.tubeset.copy()
    initial_state = tuple(tuple(tube) for tube in tubes)
    stack = [(initial_state, [])]  # Stack of (state, path)
    visited = set()

    while stack:
        current_state, path = stack.pop()

        if current_state in visited:
            continue
        visited.add(current_state)

        if check(current_state):
            return path  # Return the sequence of moves

        for i, j in getValidMoves(current_state):
            # Make the move
            new_state = [list(tube) for tube in current_state]
            
            for _ in range(countCombinedTop(new_state[i-1])):
                new_state[j-1].append(new_state[i-1].pop())
            
            new_state_tuple = tuple(tuple(tube) for tube in new_state)

            if new_state_tuple not in visited:
                stack.append((new_state_tuple, path + [(i, j)]))

    return None  # No solution found

# Time: O(b^d) | Space: O(b^d)
# b = number of valid moves on each state
# d = number of moves required
# ERROR
def bfs_solve(game:Watersort):
    tubes = game.tubeset.copy()
    initial_state = tuple(tuple(tube) for tube in tubes)
    queue = deque([(initial_state, [])])  # Queue of (state, path)
    visited = set()

    while queue:
        current_state, path = queue.popleft()

        if current_state in visited:
            continue
        visited.add(current_state)

        if check(current_state):
            return path  # Return the sequence of moves

        for i, j in getValidMoves(current_state):
            new_state = [list(tube) for tube in current_state]
            
            for _ in range(countCombinedTop(new_state[i-1])):
                new_state[j-1].append(new_state[i-1].pop())
            
            new_state_tuple = tuple(tuple(tube) for tube in new_state)

            if new_state_tuple not in visited:
                queue.append((new_state_tuple, path + [(i, j)]))
        
        return None
    
def test_algo(algo:str, game:Watersort = Watersort, show_steps = False):
    algorithms = ['a*', 'dfs', 'bfs']
    if algo not in algorithms: return None
    
    tm.start()
    start = time()
    
    solution = None
    if algo.lower() == 'a*': solution = a_star_solve(game)
    elif algo.lower() == 'dfs': solution = dfs_solve(game)
    elif algo.lower() == 'bfs': solution = bfs_solve(game)
    
    space_used = tm.get_traced_memory()
    
    end  = time()
    tm.stop()
    
    exec_time = end - start
    
    if solution is not None:
        print(colored(f"{algo.upper()} Solution: {solution}", 'green'))
        print(f"Total moves: {colored(len(solution), 'yellow')}")
        if show_steps:
            for source, target in solution:
                game.pourTo(source, target)
                game.display()
                print()
    else:
        print(f"{colored('ERROR', 'red')}: No solution found, Puzzle is {colored('UNSOLVABLE', 'red')} with {algo.upper()}")
        
    print(f"{colored(algo.upper(), 'yellow')} Solution found in {colored(f'{exec_time * 1000:.3f} ms', 'yellow')} {colored(f'({space_used[0]} bytes used)', 'light_blue')}\n")
    return solution
    
if __name__ == "__main__":
    print('================================================================')
    
    f = eval(input("Insert number of filled tubes\t: "))
    x = eval(input("Insert number of empty tubes\t: "))
    algo = input('Solver algorithm: ')
        
    while True:
        print('================================================================')
        
        print(f'Fill-Null Tubes = {f}, {x} - Total tubes = {f + x}')
        game = Watersort(f + x, x)
        print(colored('-------------- Tube Set --------------', 'yellow'))
        game.display()
        print(colored('--------------------------------------', 'yellow'))
        
        print('================================================================')
        
        if algo.lower() != 'all':
            test_algo(algo.lower(), game, True)
        else:
            test_algo('a*', game, False)
            test_algo('dfs', game, False)
            test_algo('bfs', game, False)
        
        retry = input("Retry? ('y' to retry) ")
        if retry.lower() != 'y': break
        
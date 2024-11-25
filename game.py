from random import choice
from termcolor import colored

class Watersort:
    
    def __init__(self, num_tubes = 4, null_tubes = 1, capacity = 4):
        self.colors     = ['RED', 'ONG', 'YLW', 'GRN', 'BLU', 'CYN', 'MGT', 'PNK', 'BRN', 'WHT', 'GRY', 'BLK']
        self.num_tubes  = num_tubes
        self.capacity   = capacity
        
        self.null_tubes = null_tubes
        self.fill_tubes = self.num_tubes - self.null_tubes
        
        #--------------------------------------------------------------------------------------------------------------------------------#
        
        self.game_colors = {}
        self.__generateColorSet()
        
        self.tubeset = []
        self.__generateTubeSet()
        
    # O(n)
    def __generateColorSet(self):
        for _ in range(self.fill_tubes):
            rand_color = choice(self.colors)
            self.game_colors[rand_color] = 0
            
    def __generateTubeSet(self):
        for _ in range(self.fill_tubes):
            new_tube = []
            while len(new_tube) < self.capacity:
                rand_color = choice(list(self.game_colors.keys()))
                if self.game_colors[rand_color] < self.capacity:
                    new_tube.append(rand_color)
                    self.game_colors[rand_color] += 1
                else: continue
            self.tubeset.append(new_tube)
            
        for _ in range(self.null_tubes):
            self.tubeset.append([])
            
    def __countCombinedTop(self, tube:list):
        col_count = 1
        for index in range(-2, -len(tube)-1, -1):
            if tube[index] == tube[-1]:
                col_count += 1
            else: break
        return col_count
    
    def __tubeCheck(self, tube:list):
        return len(set(tube)) <= 1 and (len(tube) == self.capacity or len(tube) == 0)
    
    def display(self):
        for tube in self.tubeset:
            text = f'Tube {self.tubeset.index(tube) + 1}: '
            if self.__tubeCheck(tube):
                text += f"{colored(tube, 'green')}"
            else:
                text += f"{colored(tube, 'red')}"
            print(text)
        
    def check(self):
        return all((len(tube) == self.capacity or len(tube) == 0) and len(set(tube)) <= 1 for tube in self.tubeset)
    
    def getValidMoves(self):
        moves = []
        for i, source in enumerate(self.tubeset):
            if not source: continue
            
            for j, target in enumerate(self.tubeset):
                
                required_space = self.__countCombinedTop(source)
                
                if i == j or (target and (target[-1] != source[-1] or len(target) + required_space > self.capacity)):
                    continue
                
                moves.append((i+1, j+1))
        return moves

    def getTubeContents(self, index:int):
        return self.tubeset[index - 1] if index > 0 else 0
            
    def pourTo(self, a:int, b:int, show_result = False):
        if (a < 0 or b < 0):
            raise IndexError('Tube index cannot be negative')
        if (a == b):
            return False
        else:
            source:list = self.getTubeContents(a)
            target:list = self.getTubeContents(b)
            
            required_space = self.__countCombinedTop(source)
            if (not target) or (target[-1] == source[-1] and len(target) + required_space <= self.capacity):
                print(f"Poured {colored(required_space, 'yellow')} {colored(source[-1], 'yellow')} from {colored(f'Tube {a}', 'yellow')} to {colored(f'Tube {b}', 'yellow')}")
                for _ in range(required_space): target.append(source.pop())
                return True
            else:
                return False
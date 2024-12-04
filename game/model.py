from typing import List
from abc import ABC, abstractmethod
from game.config import Config
import numpy as np

class Subject(ABC):
    def __init__(self):
        self.observers: List[Observer] = []
    
    def attach(self, observer: 'Observer'):
        self.observers.append(observer)

    def detach(self, observer: 'Observer'):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)

class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject):
        pass

class GameModel(Subject):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.grid: np.ndarray = np.random.choice(
                                a=[0, 1],
                                size=(config.n_cells_x, config.n_cells_y),
                                p=[0.5, 0.5])

    def next_generation(self):
        new_state = np.copy(self.grid)
        self._calculate_next_generation(new_state)
        self.grid = new_state   
        self.notify()

    def _calculate_next_generation(self, new_state: np.ndarray):
        for y in range(self.config.n_cells_y):
            for x in range(self.config.n_cells_x):
                pass
                alive_neigbors = self._count_alive_neighbours(x, y)
                new_state[x, y] = self._resolve_state(self.grid[x, y], alive_neigbors)

    def _count_alive_neighbours(self, x: int, y: int) -> int:
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                count += self.grid[(x + dx) % self.config.n_cells_x, (y + dy) % self.config.n_cells_y]
        return count
    
    def _resolve_state(self, current: int, neighbors: int) -> int:
        if current == 1 and (neighbors < 2 or neighbors > 3):
            return 0
        elif current == 0 and neighbors == 3:
            return 1
        else:
            return current

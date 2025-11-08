"""
generate_sim_env.py
- Software simulation für Q-Learning Agent Training
- Autor: Shivang Soni
"""

import random
import logging

logging.basicConfig(level=logging.INFO)


class SimEnv:
    def __init__(
            self, 
            grid_size=(5, 5),
            start_pos=(0, 0),
            obstacles: list | None = None,
            random_obstacles: bool = False,
            num_random_obstacles: int = 3
            ):
        """
        grid_size: (width, height)
        start_pos: Startposition (x, y)
        obstacles: Liste von (x,y)-Tuples, die feste Hindernisse sind
        random_obstacles: falls True, erzeuge num_random_obstacles zufällige Hindernisse
        """
        if not (isinstance(grid_size, tuple) and len(grid_size) == 2):
            raise ValueError("grid_size muss ein Tuple (width, height) sein")
        self.grid_size = grid_size
        self.start_pos = start_pos
        self.goal_pos = (grid_size[0]-1, grid_size[1]-1)

        self._fixed_obstacles = set(obstacles or [])
        self._random_obstacles = set()
        self.random_obstacles_flag = bool(random_obstacles)
        self.num_random_obstacles = int(num_random_obstacles)

        self.reset()

    def reset(self):
        """Setzt die Umgebung auf den Startzustand zurück"""
        self.position = self.start_pos

        if self.random_obstacles_flag:
            self._random_obstacles.clear()
            attempts = 0
            while len(self._random_obstacles) < self.num_random_obstacles and attempts < 100:
                rx = random.randint(0, self.grid_size[0] - 1)
                ry = random.randint(0, self.grid_size[1] - 1)
                coordinates = (rx, ry)
                if coordinates in [self.start_pos, self.goal_pos] or coordinates in self._fixed_obstacles:
                    attempts += 1
                    continue
                self._random_obstacles.add(coordinates)
                attempts += 1
       
        self.obstacles = set(self._fixed_obstacles) | set(self._random_obstacles)
        return self.position

    def _is_obstacle(self, coordinate):
        """Bestimmt, ob dieser Koordinat wirklich ein Hindernis ist"""
        return coordinate in self.obstacles
    
    def get_valid_actions(self):
        """Gibt alle gültigen Aktionen vom aktuellen Standort zurück"""
        x, y = self.position
        potential_actions = {
            0: (x, y-1),  # up
            1: (x, y+1),  # down
            2: (x-1, y),  # left
            3: (x+1, y)   # right
        }
        valid_actions = [
            a for a, (nx, ny) in potential_actions.items()
            if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]
            and (nx, ny) not in self.obstacles
        ]
        return valid_actions

    def _next_position(self, action):
        x, y = self.position 
        if action == 0: y -= 1
        elif action == 1: y += 1
        elif action == 2: x -= 1
        elif action == 3: x += 1
        return (x, y)

    def step(self, action):
        """Führt eine Aktion aus und gibt next_state, reward, done zurück"""
        new_position = self._next_position(action)

        # Ungültige Aktion → Strafe
        if (new_position[0] < 0 or new_position[0] >= self.grid_size[0] or
            new_position[1] < 0 or new_position[1] >= self.grid_size[1] or
            self._is_obstacle(new_position)):
            return self.position, -10.0, False

        self.position = new_position

        if new_position == self.goal_pos:
            return self.position, 10.0, True

        # Reward-Shaping: Fortschritt belohnen
        old_dist = abs(self.position[0] - self.goal_pos[0]) + abs(self.position[1] - self.goal_pos[1])
        new_dist = abs(new_position[0] - self.goal_pos[0]) + abs(new_position[1] - self.goal_pos[1])
        reward = 0.1 if new_dist < old_dist else -0.01
        return self.position, reward, False
     
    def render(self):
        """Textuelle Darstellung der Umgebung"""
        for y in range(self.grid_size[1]):
            row = ""
            for x in range(self.grid_size[0]):
                pos = (x, y)
                if pos == self.position:
                    row += "A "
                elif pos == self.goal_pos:
                    row += "G "
                elif pos in self.obstacles:
                    row += "X "
                else:
                    row += ". "
            print(row)
        print()

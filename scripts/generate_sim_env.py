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
        random_obstacles: falls True 
        dann erzeuge num_random_obstacles zufällige Hindernisse
        num_random_obstacles: Anzahl zufälliger Hindernisse
        (aber nur wenn random_obstacles True)
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
        """
        Setzt die Umgebung auf den Startzustand zurück.
        """
        self.position = self.start_pos

        if (self.random_obstacles_flag):
            self._random_obstacles.clear()
            attempts = 0
            while (len(self._random_obstacles)<self.num_random_obstacles and attempts < 100):
                rx = random.randint(0, self.grid_size[0] - 1)
                ry = random.randint(0, self.grid_size[1] - 1)
                coordinates = (rx, ry)
                # Nie wähle Start- oder Endpunkt als Hindernis
                if coordinates == self.start_pos or coordinates == self.goal_pos:
                    attempts += 1
                    continue
                # Keine Überschneidung mit festen Hindernissen
                if coordinates in self._fixed_obstacles:
                    attempts += 1
                    continue
                self._random_obstacles.add(coordinates)
                attempts += 1
                #logging.info(f"Hindenis bei {coordinates} vorhanden.")
       
        self.obstacles = set(self._fixed_obstacles) | \
            set(self._random_obstacles)

        return self.position

    def _is_obstacle(self, coordinate):
        """
        Bestimmt, ob dieser Koordinat wirklich ein Hindernis.
        """
        return coordinate in self.obstacles
    
    def get_valid_actions(self):
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
        if action == 0: 
            return (x, y-1)
        elif action == 1:
            return (x, y+1)
        elif action == 2:
            return (x-1, y)
        elif action == 3:
            return (x+1, y)
        else:
            return (x, y)

    def step(self, action):
        """
        action: 0=up, 1=down, 2=left, 3=right
        return: next_state, reward, done
        """
        x, y = self.position
        if action == 0 and y > 0:  # up
            y -= 1
        elif action == 1 and y < self.grid_size[1] - 1:  # down
            y += 1
        elif action == 2 and x > 0:  # left
            x -= 1
        elif action == 3 and x < self.grid_size[0] - 1:  # right
            x += 1
        else:
            logging.warning(
                f"Ungültige Aktion {action} an Position {self.position}"
                )
            return self.position, -5.0, False
   
        new_position = (x, y)

        if self._is_obstacle(new_position):
            return self.position, -5.0, False

        if new_position == self.goal_pos:
            self.position = self.goal_pos
            return self.position, 10.0, True
      
        self.position = new_position
        return self.position, -0.01, False
     
    def render(self):
        for y in range(self.grid_size[1]):
            row = ""
            for x in range(self.grid_size[0]):
                pos = (x, y)
                if pos == self.position:
                    row += "A "  # Agent
                elif pos == self.goal_pos:
                    row += "G "
                elif pos in self.obstacles:
                    row += "X "
                else:
                    row += ". "
            print(row)
        print()


if __name__ == "__main__":
    env = SimEnv()
    state = env.reset()
    logging.info(f"Start State: {state}")
    for _ in range(15):
        valid_actions = []
        x, y = env.position

        if y > 0:
            valid_actions.append(0)  # up
        if y < env.grid_size[1] - 1:
            valid_actions.append(1)  # down
        if x > 0:
            valid_actions.append(2)  # left
        if x < env.grid_size[0] - 1:
            valid_actions.append(3)  # right

        action = random.choice(valid_actions)
        next_state, reward, done = env.step(action)

        if next_state == state:
            continue

        if done:
            logging.info(
                f"Reached goal at state: {next_state} with reward: {reward}"
                )
            break
        else:
            logging.info(f"Next State: {next_state}, Reward: {reward}")
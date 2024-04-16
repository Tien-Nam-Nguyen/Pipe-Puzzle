# ASSIGNMENT 1: AI INTRODUCTION

## Bridges puzzle (Hashi)

- Step 1: Install the `pygame` library

```bash
pip install pygame
```

Note: **(WIP) CLI only**

- Step 2: Create a game state

```python
from bridges_puzzle import create_game, stringify, Bounds

# Create a game with 10 anchors and a 3x3 grid
bounds = Bounds(3, 3, 0, 0)
anchor_count = 10

game = create_game(anchor_count, bounds)

# Increased difficulty. How often two anchors are connected using double bridges.
game = create_game(anchor_count, bounds, 5)

# Available values: [0, 9]. Defaults to 0.
# *Note*: A difficulty of 0 doesn't guarantee all bridges are single. It only suggests that the majority of bridges are single.
# *Note*: A difficulty of 9 will try to upgrade all bridges to be double bridges.

# Print the abbreviated game state
print(f"Game: {game}")

# Pretty print the game state
print(stringify(game))

# Pretty print the game state, showing coordinates
print(stringify(game, show_coordinates=True))

```

# ASSIGNMENT 1: AI INTRODUCTION

## Bridges puzzle (Hashi)

### Step 1: Install the `pygame` library

```bash
pip install pygame
```

### Step 2: **(WIP) CLI only** Create a game state

Game generation supports custom level dimensions and anchor count. The difficulty parameter is optional and can be used to increase the likelihood of double bridges being used.

Available difficulty levels go from 0 to 9 and defaults to 0.

**Notes**:

- A difficulty of 0 doesn't guarantee all bridges are single. It only suggests that the majority of bridges are single. A difficulty of 9 will try to upgrade all bridges to be double bridges.
- `create_game(...)` returns a `GameState` that has already been solved. You can call `reset(game_state)` to get a copy of the game state in its initial state.

```python
from bridges_puzzle import create_game, stringify, reset, Bounds

# Create a game with 10 anchors and a 3x3 grid
bounds = Bounds(3, 3, 0, 0)
anchor_count = 10

# Generate a game state (solved already)
solution = create_game(anchor_count, bounds)

# Increased difficulty. How often two anchors are connected using double bridges.
solution = create_game(anchor_count, bounds, 5)

# Reset the game state to its initial state
game = reset(solution)

# Print the abbreviated game state
print(f"Game: {game}")

# Pretty print the game state
print(stringify(game))

# Pretty print the game state, showing coordinates
print(stringify(game, show_coordinates=True))

```

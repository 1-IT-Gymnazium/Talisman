# Talisman

Welcome to the GitHub repository for Talisman, a board game designed for up to 4 players. The game is filled with fighting, collecting, and leveling elements.

## Installation

To install the game, follow these steps:

1. Download `Talisman.zip` from the releases section.
2. Unzip the contents into a folder.
3. Install the necessary dependencies.
4. Run `Talisman.exe` to start playing!

## Game Overview

The game starts by selecting the number of players and characters. Character stats are available in the documentation.

## How to Play

- **Movement**: Use the arrow keys on your keyboard.
- **Dice Roll**: Press the spacebar to roll the dice and determine your move count.
- **Drawing Cards**: Press `D` on your keyboard. Cards can be enemies, objects, or followers, affecting gameplay accordingly.
- **Combat**: In fights, roll the dice for the enemy and then for yourself. Press the spacebar again to see the result of the fight.
- **Popup Windows**: Interact with popup windows in various sections like the Village, City, Tavern, and Chapel for different actions. Close the popup by performing a game-related action.

### Sections

- **Adventure Sections**: Forest, Graveyard, Cracks, ElvForest, Ruins.
- **Interaction Sections**: Village, City, Tavern, Chapel.
- **Combat Section**: Sentinel.

## File Structure

- `Talisman.exe` - The game launcher.
- `main.py` - Initializes and runs the game.
- `game_events.py` - Handles game events.
- `Cards.py` - Manages card data.
- `button.py` - Enables button functionality on the UI.
- Directories for different types of cards and game assets (`EnemyCards/`, `FollowerCards/`, etc.).

## Dependencies

Ensure the following dependencies are installed before running the game:

- Python 3.10
- Pygame
- OS (usually comes with Python)

### Installing Python

Download and install Python 3.10 from the official Python website. Make sure to add Python to your system's PATH.

### Installing Pygame and Other Libraries

After installing Python, install Pygame using pip:

```bash
pip install pygame

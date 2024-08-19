# 🐪 Camel Up in Python 🏁

<img src="https://cf.geekdo-images.com/1ph2jVOD1MudR1fK1nkwwA__itemrep/img/x5pEGB463NY3DOzCUC7wfU0itrI=/fit-in/246x300/filters:strip_icc()/pic2031446.png" width="40%">

## Authors
- Adeline Greene [@AdelineG218](https://github.com/AdelineG218)
- Anish Goyal [@anishgoyal1108](https://github.com/anishgoyal1108)

## Introduction
### What is Camel Up?
**Camel Up** is a lively and engaging game where two players bet on camels racing around a track. We've brought the fun of Camel Up to Python, allowing you to experience the excitement of the race right from your terminal! 🎲

<img src="https://i.imgur.com/jfIo1er.png">

### How To Play
To start the game, simply clone this repo and run `python main.py`. From the main menu, select "Start New Game" and enter the names of both players.

## How We Made the Game
### Classes
Our implementation of Camel Up is structured with several key classes that are each defined in their own separate Python modules:
- **Player**: Represents a player in the game, handling individual actions like placing bets or rolling dice.
- **GameManager**: Manages the overall state and rules of the game, coordinating between players and ensuring the game runs smoothly.
- **MainMenu**: Displays the main menu and handles user choices, such as starting a new game or exiting.
- **PlayGame**: Manages the gameplay, including displaying the game state and processing player actions during the game.
- **EVBot**: A strategic assistant that provides hints for betting on each camel.

### Interaction Between Classes
- `MainMenu` interacts with `GameManager` to start the game when a new game is selected.
- `GameManager` interacts with `Player` to manage player-specific actions and details. It also provides game state details to `PlayGame` for display and interaction.
- `PlayGame` communicates with `GameManager` to execute game actions such as moving camels, updating scores, and switching turns. It also engages with `EVBot` to provide strategic hints to players during the game.

## Our Addition
In our Pythonic version of Camel Up, we've added a strategic twist by incorporating Expected Value (EV) calculations within the `EVBot` class. By running Monte Carlo simulations, we can determine the probability of each camel winning or placing second. Players can pay one coin to get a hint on the best camel to bet on based on these probabilities!

<img src="https://i.imgur.com/Mgf8AMP.png">

### How It Works
1) Simulate moving each camel across possible board states for a set of dice rolls and orders.
2) Determine the winner and runner-up camels from the simulated board states with `find_simulated_winner`.
3) Keep track of the number of times each camel wins and finishes second across all simulations.
4) Compute the EV for each camel based on win and runner-up probabilities, along with the value of the bet if the camel is in the game.
5) Identify the camel with the highest EV and generate a recommendation for which camel to bet on (or if rolling is preferable to begin with).

## Conclusion
Feel free to explore the code and enjoy the thrill of Camel Up in Python with your friends! Thank you to Jane Street Capital Group for giving us the opportunity to make this project.

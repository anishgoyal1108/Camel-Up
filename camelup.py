from gamemanager import GameManager
from player import Player
import colorama
import os

def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
class PlayGame:
    def __init__(self, game_manager: GameManager):
        self.game = game_manager
        self.current_player = game_manager.current_player
        self.current_name = game_manager.player_names[0]
        self.color_dict =        {
            "RED": colorama.Fore.RED,
            "GREEN": colorama.Fore.GREEN,
            "BLUE": colorama.Fore.BLUE,
            "YELLOW": colorama.Fore.YELLOW,
            "PURPLE": colorama.Fore.MAGENTA
        }

    
    def take_turn(self) -> None:
        while True:
            action = input(f"\n{self.current_name}'s turn!\n(B)et or (R)oll? ").upper()
            if action != "B" and action != "R":
                print("Sorry, that's not a valid move.")
                continue
            else:
                break
        
        if action == "B":
            while True:
                color = input("Which bet would you like to place? (red, green, blue, yellow, purple) ").lower()
                if color != "red" and color != "green" and color != "blue" and color != "yellow" and color != "purple":
                    print("Sorry, that's not a valid card.")
                    continue
                elif len(self.game.cards[color]) == 0:
                    print(f"Sorry, all the {color} cards are gone.")
                    continue
                else:
                    break
            self.game.cards = self.current_player.take_bet(color, self.game.cards)
        else:
            available_dice = [key for key in self.game.dice if self.game.dice[key] == 0]
            color, number = self.current_player.roll(available_dice)
            self.game.dice[color] = number
        
        if self.current_player == self.game.players[0]:
            self.current_name = self.game.player_names[1]
            self.current_player = self.game.players[1]
        else:
            self.current_name = self.game.player_names[0]
            self.current_player = self.game.players[0]

    def display_game(self) -> None:
        clear()
        colorama.init(autoreset=True)
        print("   Ticket Tents: ", end="")
        for key in ["red", "green", "blue", "yellow", "purple"]:
            if len(self.game.cards[key]) != 0:
                print(self.color_dict[key.upper()] + str(max(self.game.cards[key])), end=" ")
            else:
                print(self.color_dict[key] + "X", end=" ")
        print(" " * 10, end=" ")
        print("Dice Tents: ", end="")
        for die in ["red", "green", "blue", "yellow", "purple"]:
            if self.game.dice[die] != 0:
                print(self.color_dict[die.upper()] + str(self.game.dice[die]), end=" ")
            else:
                print(self.color_dict[die.upper()] + "_", end=" ")
        print()
        print
        for _ in range(5):
            print("🌴" + " " * 58 + "🏁")
        print("    ", end="")
        for i in range(1, 17):
            print(str(i) + " ", end=" ")
        print()
        print()
        print("   ", end="") 
        spacer = 0
        if self.game.player_scores[0] > 9:
            spacer = 1
        print(f"{self.game.player_names[0]} has {self.game.player_scores[0]} coins." + " " * (22 - spacer), end="")
        print(f"{self.game.player_names[1]} has {self.game.player_scores[1]} coins.")
        print("   ", end="")
        print("Bets: ", end="")
        count = 0
        for key in self.game.players[0].cards:
            for i in self.game.players[0].cards[key]:
                print(self.color_dict[key.upper()] + str(i), end=" ")
                count += 1
        print(" " * (34 - 2 * count), end="")
        print("Bets: ", end="")
        for key in self.game.players[1].cards:
            for i in self.game.players[1].cards[key]:
                print(self.color_dict[key.upper()] + str(i), end=" ")
        print()
        

if __name__ == "__main__":
    game = GameManager()
    play_game = PlayGame(game)
    num_dice_rolled = 0
    while num_dice_rolled > 0:
        play_game.display_game()
        play_game.take_turn()
    print("End Game")
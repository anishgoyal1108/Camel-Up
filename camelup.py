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
        self.num_dice_rolled = 0
    
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
            self.num_dice_rolled += 1
            self.game.move_camels(color, number)
        
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
        print() 
        for row in range(4, -1, -1):
            print("🌴  ", end="")
            for pos in range(16):
                if len(self.game.board[pos]) > row:
                    camel = self.game.board[pos][row]
                    if len(camel) != 0:
                        if pos <= 8:
                            print(self.color_dict[camel.upper()] + camel[0][0].upper(), end="  ")
                        else:
                            print(self.color_dict[camel.upper()] + camel[0][0].upper(), end="   ")
                elif pos <= 8:
                    print("   ", end="")
                else:
                    print("    ", end="")
            print("🏁")
        print("    ", end="")
        for i in range(1, 17):
            print(str(i) + " ", end=" ")
        print()
        print()
        print("   ", end="") 
        spacer = 0
        if self.game.players[0].coins > 9:
            spacer = 1
        print(f"{self.game.player_names[0]} has {self.game.players[0].coins} coins." + " " * (22 - spacer), end="")
        print(f"{self.game.player_names[1]} has {self.game.players[0].coins} coins.")
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
    
    def display_final(self) -> None:
        winning_player = None

        self.game.update_score()

        spacer = 0
        if self.game.player_scores[0] > 9:
            spacer = 1
        print(f"{self.game.player_names[0]} has {self.game.player_scores[0]} coins." + " " * (22 - spacer), end="")
        print(f"{self.game.player_names[1]} has {self.game.player_scores[1]} coins.")
        if (self.game.player_scores[0] > self.game.player_scores[1]):
            print(f"{self.game.player_names[0]} has won!")
        elif (self.game.player_scores[1] > self.game.player_scores[0]):
            print(f"{self.game.player_names[1]} has won!")
        else:
            print(f"{self.game.player_names[0]} and {self.game.player_names[1]} have tied!")
        

if __name__ == "__main__":
    game = GameManager()
    play_game = PlayGame(game)
    game.init_camels()
    while play_game.num_dice_rolled < 5:
        play_game.display_game()
        play_game.take_turn()
    winning_camel_found = False
    for i in range(15, 0, -1):
        if len(game.board[i]) > 0:
            if not winning_camel_found:
                game.winning_camel = game.board[i][-1]
                winning_camel_found = True
            else:
                game.second_camel = game.board[i][-1]
                break
    play_game.display_final()
    print("End Game")
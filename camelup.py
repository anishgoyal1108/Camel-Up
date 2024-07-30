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
            if action == "BET":
                action = "B"
                break
            elif action == "ROLL":
                action = "R"
                break
            elif action != "B" and action != "R":
                print("Sorry, that's not a valid move.")
                continue
            else:
                break
        
        if action == "B":
            camel = ["red", "green", "blue", "yellow", "purple"]
            camel_short = ["r", "g", "b", "y", "p"]
            while True:
                color = input("Which bet would you like to place? (red, green, blue, yellow, purple) ").lower() 
                if color in camel_short:
                    color = camel[camel_short.index(color)]
                    break
                elif color not in camel:
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
        colorama.init(autoreset=True)
        game_state = []

        # Print Ticket Tents
        game_state.append("   Ticket Tents: ")
        for key in ["red", "green", "blue", "yellow", "purple"]:
            if len(self.game.cards[key]) != 0:
                game_state.append(self.color_dict[key.upper()] + str(max(self.game.cards[key])) + " ")
            else:
                game_state.append(self.color_dict[key.upper()] + "X ")
        game_state.append(" " * 10)
        
        # Print Dice Tents
        game_state.append(colorama.Fore.WHITE + "Dice Tents: ")
        for die in ["red", "green", "blue", "yellow", "purple"]:
            if self.game.dice[die] != 0:
                game_state.append(self.color_dict[die.upper()] + str(self.game.dice[die]) + " ")
            else:
                game_state.append(self.color_dict[die.upper()] + "_ ")
        game_state.append("\n\n")
        
        # Print the game board
        for row in range(4, -1, -1):
            game_state.append("🌴  ")
            for pos in range(16):
                if len(self.game.board[pos]) > row:
                    camel = self.game.board[pos][row]
                    if len(camel) != 0:
                        if pos <= 8:
                            game_state.append(self.color_dict[camel.upper()] + camel[0][0].upper() + "  ")
                        else:
                            game_state.append(self.color_dict[camel.upper()] + camel[0][0].upper() + "   ")
                elif pos <= 8:
                    game_state.append("   ")
                else:
                    game_state.append("    ")
            game_state.append("🏁\n")
        
        # Print board positions
        game_state.append("    " + colorama.Fore.WHITE)
        for i in range(1, 17):
            game_state.append(str(i) + "  ")
        game_state.append("\n\n")
        
        # Print player info
        game_state.append("   ")
        spacer = 0
        if self.game.players[0].coins > 9:
            spacer = 1
        game_state.append(f"{self.game.player_names[0]} has {self.game.players[0].coins} coins." + " " * (22 - spacer))
        game_state.append(f"{self.game.player_names[1]} has {self.game.players[1].coins} coins.\n")
        
        # p1 bets
        game_state.append(colorama.Fore.WHITE + "   Bets: ")
        count = 0
        for key in self.game.players[0].cards:
            for i in self.game.players[0].cards[key]:
                game_state.append(self.color_dict[key.upper()] + str(i) + " ")
                count += 1
        game_state.append(" " * (34 - 2 * count))
        
        # p2 bets
        game_state.append(colorama.Fore.WHITE + "Bets: ")
        for key in self.game.players[1].cards:
            for i in self.game.players[1].cards[key]:
                game_state.append(self.color_dict[key.upper()] + str(i) + " ")
    
        # final print statement 
        print("".join(game_state)) 
    
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
    while game.winning_camel == "":
        clear()
        play_game.display_game()
        play_game.take_turn()
        if play_game.num_dice_rolled == 5:
            leg_ended = []
            leg_ended.append(" " * 34 + "LEG ENDED!\nLeg Results:\n")
            init_player1_coins = game.players[0].coins
            init_player2_coins = game.players[1].coins
            game.update_score()
            game.players[0].coins = game.player_scores[0]
            game.players[1].coins = game.player_scores[1]
            spacer = 0
            if game.player_scores[0] > 9:
                spacer += 1
            if abs(game.player_scores[0]-init_player1_coins) > 9:
                spacer += 1
            if game.player_scores[0]-init_player1_coins < 0:
                spacer += 1
            leg_ended.append("🥇 FIRST PLACE 🥇: " + play_game.color_dict[game.winning_camel.upper()] + game.winning_camel.upper() + "\n")
            leg_ended.append("🥈 SECOND PLACE 🥈: " + play_game.color_dict[game.second_camel.upper()] + game.second_camel.upper() + "\n")
            leg_ended.append(f"{game.player_names[0]} has {game.player_scores[0]} coins ({game.player_scores[0]-init_player1_coins} coins)." + " " * (13 - spacer) + "\n")
            leg_ended.append(f"{game.player_names[1]} has {game.player_scores[1]} coins ({game.player_scores[1]-init_player2_coins} coins).\n")
            print(''.join(leg_ended))
            input("Press any key to continue... ")
            play_game.num_dice_rolled = 0
            game.leg_reset()
    
    '''winning_camel_found = False
    for i in range(15, 0, -1):
        if len(game.board[i]) > 0:
            if not winning_camel_found:
                game.winning_camel = game.board[i][-1]
                winning_camel_found = True
            else:
                game.second_camel = game.board[i][-1]
                break'''
    play_game.display_final()
    print("End Game")
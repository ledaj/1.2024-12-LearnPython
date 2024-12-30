import random
import logging

# Variables de base
board = ["-" for x in range(9)]
player = 'X'
is_WinState = False
is_DrawState = False

def print_board(): # créer les neufs cases

    row1 = "|{}|{}|{}|".format(board[0], board[1], board[2])
    row2 = "|{}|{}|{}|".format(board[3], board[4], board[5])
    row3 = "|{}|{}|{}|".format(board[6], board[7], board[8])
    
    #impression du tableau
    print()
    print(row1)
    print(row2)
    print(row3) 
    print() 

def swapPlayer(player) : #changer de joueur
    return 'X' if player == 'O' else 'O'

def playerMove(player): # Tour de jeu
    print("Your turn, player {}.".format(player))
    print()
    print_board()
    print()
    while True:
        try:
            choice = int(input("Enter your move (1-9) : ").strip())
            if choice in range(1,9):
                if board[choice - 1] == "-":
                    board[choice - 1] = player
                    print()
                    print("Player {}, in {}".format(player,choice))
                    print()
                    break
                else:
                    print()    
                    print("That space is already taken.")
                    print("Try again player {}.".format(player))                       
            else:
                print()
                print("Not a valid number.")
                print("Try again player {}.".format(player))
                print("Try again player {}.".format(player))
                print()
        except:        
            print()
            print("Not a number.")
            print("Try again player {}.".format(player))
            print() 

def gameStart(player, board): # sert à relancer une partie
    # tirage du premier joueur
    randomNumber = random.randint(0, 1)
    player = 'X' if randomNumber == 1 else 'O'
    
    #reset de toutes les cases
    while "X" in board:
            for X in range(0,8):
                board[X] = "-"
    
    print("Player {} starts !".format(player))    
    print()
    gameLoop(player)


def is_WinState(player): # Conditions de victoire
        # ligne entière ?
        if board[0] == board[1] == board[2] == player:
            return True
        elif board[3] == board[4] == board[5] == player:
            return True
        elif board[6] == board[7] == board[8] == player:
            return True
        # colonne entière ?
        elif board[0] == board[3] == board[6] == player:
            return True
        elif board[1] == board[4] == board[7] == player:
            return True
        elif board[2] == board[5] == board[8] == player:
            return True
        # diagonale entière ?
        elif board[0] == board[4] == board[8] == player:
            return True
        elif board[2] == board[4] == board[6] == player:
            return True
        else:
            return False

def is_DrawState(board): # vérifie si toutes les cases sont pleines
    return True if "-" not in board else False
    
def gameLoop(player): # Boucle de jeu
    while True:
        if is_WinState("X") == True: # victoire atteinte pour X ?
            print()
            print_board()
            print()
            print("Game Over.")
            print("Player X WINS !")
            newGame(player,board)
            break
        elif is_WinState("O") == True: # victoire atteinte pour O ?
            print()
            print_board()
            print()
            print("Game Over.")
            print ("Player O WINS !")
            newGame(player,board)
            break
        elif is_DrawState(board) == True: # le tableau est plein ?
            print("Game Over.")
            print ("Nobody wins.")
            newGame(player,board)
            break
        else: # on continue à jouer
            playerMove(player)
            player = swapPlayer(player)
    
def newGame(player,board): # Choix d'une nouvelle partie
    print("Try again ?")
    print()
    while True:
        try:
            answer = str(input("(Y/N) : ").strip())
            if answer == "Y":
                gameStart(player, board)
            elif answer == "N":
                print("Thanks for playing.")
                break
        except:        
            print()
            print("Not a valid answer.")
            print() 

#Init
gameStart(player, board)
gameLoop(player)

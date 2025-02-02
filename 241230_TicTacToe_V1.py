import random
import logging

# Variables de base
board = ["-" for x in range(9)]
player = 'X'
is_WinState = False
is_GameOver = False

def printBoard(): 
  # POUR créer le tableau à 9 cases je crée troiw lignes de trois cases

    row1 = "|{}|{}|{}|".format(board[0], board[1], board[2])
    row2 = "|{}|{}|{}|".format(board[3], board[4], board[5])
    row3 = "|{}|{}|{}|".format(board[6], board[7], board[8])
    
    #POUR afficher le tableau je l'imprime avec du vide autour
    print()
    print(row1)
    print(row2)
    print(row3) 
    print() 

def swapPlayer(player) : 
  # POUR changer de joueur j'examine la valeur du player
    return 'X' if player == 'O' else 'O'

def playerMove(player): 
  # POUR jouer son tour, j'affiche le tableau, je recueille le choix du joueur et je le remplace dans le tableau
    print("Your turn, player {}.".format(player))
    print()
    printBoard()
    print()
    while True:
        try:
            choice = int(input("Enter your move (1-10) : ").strip())
            if choice in range(1,10):
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

def gameStart(player, board): 
  #POUR lancer la partie, je tire le premier joueur
    randomNumber = random.randint(0, 1)
    player = 'X' if randomNumber == 1 else 'O'
    
    #et je vide le tableau
    while "X" in board:
            for X in range(0,8):
                board[X] = "-"
    
    print("Player {} starts !".format(player))    
    print()
    gameLoop(player)


def is_WinState(player): # POUR déteminer la victoire: 
        # je vérifie les lignes entières ?
        if board[0] == board[1] == board[2] == player:
            return True
        elif board[3] == board[4] == board[5] == player:
            return True
        elif board[6] == board[7] == board[8] == player:
            return True
        # les colonnes entières ?
        elif board[0] == board[3] == board[6] == player:
            return True
        elif board[1] == board[4] == board[7] == player:
            return True
        elif board[2] == board[5] == board[8] == player:
            return True
        # les diagonales entières ?
        elif board[0] == board[4] == board[8] == player:
            return True
        elif board[2] == board[4] == board[6] == player:
            return True
        else:
            return False

def is_GameOver(board): # POUR vérifier la fin de partie, je vérifie si toutes les cases sont pleines
    return True if "-" not in board else False
    
def gameLoop(player): # Boucle de jeu
    while True:
        if is_WinState("X") == True: # victoire atteinte pour X ?
            print()
            printBoard()
            print()
            print("Game Over.")
            print("Player X WINS !")
            newGame(player,board)
            break
        elif is_WinState("O") == True: # victoire atteinte pour O ?
            print()
            printBoard()
            print()
            print("Game Over.")
            print ("Player O WINS !")
            newGame(player,board)
            break
        elif is_GameOver(board) == True: # le tableau est plein ?
            print("Game Over.")
            print ("Nobody wins.")
            newGame(player,board)
            break
        else: # on continue à jouer
            playerMove(player)
            player = swapPlayer(player)
    
def newGame(player,board): # POUR relancer une nouvelle partie, je demande au joueur et lance gameStart ou break en fonction
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

import random
import logging

# Variables de base
board = ["-" for x in range(9)] #le tableau est une liste de 0 à 8
player = 'X'

def printBoard(): 
  # POUR afficher le tableau à 9 cases je crée trois strings qui affichent le contenu du tableau et je les imprime

    row1 = "|{}|{}|{}|".format(board[0], board[1], board[2])
    row2 = "|{}|{}|{}|".format(board[3], board[4], board[5])
    row3 = "|{}|{}|{}|".format(board[6], board[7], board[8])
    
    print()
    print(row1)
    print(row2)
    print(row3) 
    print() 

def swapPlayer() : 
  # POUR changer de joueur j'examine la valeur du player
    return 'X' if player == 'O' else 'O'

def declareActivePlayer():
    print("Your turn, player {}.".format(player))

def getValidInput():
    while True :
        try:
            Input = input("Enter your move (1-9) : ").strip()
            playerInput = int(Input) - 1

            if playerInput not in range(0,9):
                print()    
                print("Out of range.")
                print("Try again player {}.".format(player)) 
                print()

            if board [playerInput] != "-":
                    print()
                    print("That space is already taken.")
                    print("Try again player {}.".format(player)) 
                    print()

            else:
                return playerInput
        
        except ValueError:
            print()
            print("Not a number.")
            print("Try again player {}.".format(player))
            print()           

def isBoardCellEmpty(input):
     if board [input - 1] == "-":
         return True


def playerMove(player): 
  # POUR jouer son tour, j'affiche le tableau, je recueille le choix du joueur et je le remplace dans le tableau
    declareActivePlayer()

    printBoard()

    choice = getValidInput()
    board[choice] = player

    print()
    print("Player {}, in {}".format(player,choice))
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


def isWinState(player): # POUR déteminer la victoire: 
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

def isGameOver(): # POUR vérifier la fin de partie, je vérifie si toutes les cases sont pleines
    return True if "-" not in board else False
    
def gameLoop(player): # Boucle de jeu
    while True:
        if isWinState("X") == True: # victoire atteinte pour X ?
            print()
            printBoard()
            print()
            print("Game Over.")
            print("Player X WINS !")
            newGame(player,board)
            break
        elif isWinState("O") == True: # victoire atteinte pour O ?
            print()
            printBoard()
            print()
            print("Game Over.")
            print ("Player O WINS !")
            newGame(player,board)
            break
        elif isGameOver() == True: # le tableau est plein ?
            print("Game Over.")
            print ("Nobody wins.")
            newGame(player,board)
            break
        else: # on continue à jouer
            playerMove(player)
            player = swapPlayer()
    
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

import socket
import random
from random import choice
from pickle import dumps, loads
from pprint import pprint

HOST, PORT = "0.0.0.0", 8000  # defined for now
BUFFSIZE = 1024                 # for socket.send & recv commands
BACKLOG = 2                     # number of clients supported by server
SECONDS = 3                     # seconds until socket.timeout (notimplemented)
# moves dict to translate 'rps' choice
MOVES = {'1','2','3','4','5','6','7','8','9'}
# outcome dict stores result for all possible scenarios
winning_combos = [[0,1,2],  # Horizontal
                      [3,4,5],
                      [6,7,8],
                      [0,3,6],  # Vertical
                      [1,4,7],
                      [2,5,8],
                      [0,4,8],  # Diagonal
                      [2,4,6]]

def main_menu(game):
    """ initialize game dict variables & opening screen of the game
"""
    game['total'] = 0           # total number of games played
    game['won'] = 0             # total games won by player
    game['lost'] = 0            # total games lost by player
    game['drew'] = 0            # total games drew by player
    game['move'] = ''           # player's move (rps)
    game['message'] = ''        # player's chat message
    game['sentmessage'] = ''    # player's previous message
    game['start'] = True        # setting up the game boolean

    print("\tTic-Tac-Toe\n")
    if game['name']=='':        # if returning to menu don't display the following
        game['name'] = get_name()
        print("Welcome "+game['name'])

    print("1. Play single player game")
    print("2. Start two player game")
    print("3. Join two player game")
    print("4. Quit")
    print()
    c = safe_input("Your choice? ", "1234")
    c = int(c)
    if c==1:
        one_player(game)
    elif c==2:
        start_two_player(game)
    elif c==3:
        two_player_join(game)
    else:
        print('Play again soon.')

def safe_input(prompt, values='abcdefghijklmnopqrstuvwxyz'):
    """ gives prompt, checks first char of input, assures it meets
given values
        default is anything goes """
    while True:
        i = input(prompt)
        try:
            c = i[0].lower()
        except IndexError:  # the only possible error?!
            if c=='':
                print("Try again.")
        else:
            if c not in values: # some other character
                print("Try again.")
            else:   # looks good. continue.
                break
    return i

def get_name():
    """ returns input as name """
    while True:
        name = input("What is your name? ")
        check = input(name + ". Correct (y/n)? ")
        if check[0] in 'yY':
            break
    return name

def get_result(player, opponent):
    """ reports opponent's choice;
        checks player and opponent dicts ['move'] against OUTCOME
dict;
        reports result
        returns player dict with updated values """
    print(opponent['name'], 'chose %s.' % (MOVES[opponent['move']]))
    # check lookout dict (OUTCOME dictionary)
    result = OUTCOME[(player['move'], opponent['move'])]
    # update game variables
    player['total'] += 1
    if result=='win':
        print('%s beats %s. You win.' % (MOVES[player['move']], MOVES[opponent['move']]))
        player['won'] += 1
    elif result=='draw':
        print('%s - %s: no one wins. You draw.' % (MOVES[player['move']], MOVES[opponent['move']]))
        player['drew'] += 1
    else:
        print('%s loses to %s. You lose.' % (MOVES[player['move']],MOVES[opponent['move']]))
        player['lost'] += 1
    return player #SEE IF WE NEED!!!

def drawBoard(board):
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')

def inputPlayerLetter():
        letter = ''
        while not (letter == 'X' or letter == 'O'):
            print('Do you want to be X or O?')
            letter = input().upper()
            if letter == 'X':
                return ['X', 'O']
            else:
                return ['O', 'X']

def whoGoesFirst():
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'

def whoGoesFirstPVP():
        if random.randint(0, 1) == 0:
            return 'player1'
        else:
            return 'player2'

def playAgain():
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

def makeMove(board, letter, move):
        board[move] = letter

def isWinner(bo, le):
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
                (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
                (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
                (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
                (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
                (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
                (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
                (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
        dupeBoard = []
        for i in board:
            dupeBoard.append(i)
        return dupeBoard

def isSpaceFree(board, move):
        return board[move] == ' '

def getPlayerMove(board):
        move = ' '
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
            print('What is your next move? (1-9)')
            move = input()
        return int(move)

def chooseRandomMoveFromList(board, movesList):
        possibleMoves = []
        for i in movesList:
            if isSpaceFree(board, i):
                possibleMoves.append(i)
            if len(possibleMoves) != 0:
                return random.choice(possibleMoves)
            else:
                return None

def getComputerMove(board, computerLetter):

        if computerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'

        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, computerLetter, i)
                if isWinner(copy, computerLetter):
                    return i

        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, playerLetter, i)
                if isWinner(copy, playerLetter):
                    return i
        move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
        if move != None:
            return move

        if isSpaceFree(board, 5):
            return 5
        return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
        for i in range(1, 10):
            if isSpaceFree(board, i):
                return False
        return True

def one_player(game):
    """ implements one player game with minimal opponent dict """

    opponent = {}
    opponent['name'] = 'Computer'



    print('Welcome to Tic Tac Toe!')

    while True:
        theBoard = [' '] * 10
        playerLetter, computerLetter = inputPlayerLetter()
        turn = whoGoesFirst()
        print('The ' + turn + ' will go first.')
        gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'

        else:

            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player'

        if not playAgain():
            break

def start_two_player(game):
    """ starts tcp server and implements two player game
        game dict = player 1"""
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(BACKLOG)
    serverip, serverport = sock.getsockname()
    print("Running at %s, %s" % (serverip, serverport))
    print("Waiting for player...")

    client, address = sock.accept()
    clientip, clientport = address
    # server/game loop
while True:
    try:
        P2game = loads(client.recv(BUFFSIZE))
    except EOFError:
            print(P2game['name'], "left the game.")
            break
    client.send(dumps(game))


    theBoard = [' '] * 10
    p1Letter, p2Letter = inputPlayerLetter()
    turn = whoGoesFirstPVP()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player1':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player2'

        else:

            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'player1'

    if not playAgain():
        break
    # exit loop
    client.close()

    main_menu(game)

def two_player_join(game):
    """ joins a tcp server two player game
        game dict = player 2"""
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))


    # client/game loop
    while True:
        sock.send(dumps(game))
        try:
            P1game = loads(sock.recv(BUFFSIZE))
        except EOFError:
            print(P1game['name'], "left the game.")
            break
        theBoard = [' '] * 10
        p1Letter, p2Letter = inputPlayerLetter()
        turn = whoGoesFirstPVP()
        print('The ' + turn + ' will go first.')
        gameIsPlaying = True

        while gameIsPlaying:
            if turn == 'player1':
                drawBoard(theBoard)
                move = getPlayerMove(theBoard)
                makeMove(theBoard, playerLetter, move)
                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player2'

            else:

                drawBoard(theBoard)
                move = getPlayerMove(theBoard)
                makeMove(theBoard, playerLetter, move)
                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        print('The game is a tie!')
                        break
                    else:
                        turn = 'player1'

        if not playAgain():
            break
    # exit loop
    sock.close()
    print('\nYou won %s, lost %s, drew %s (%s total)\n' % \
          (game['won'],game['lost'],game['drew'],game['total']))
    main_menu(game)

if __name__=='__main__':
    game = {}               # initialize game dict to store all game variables
    game['name'] = ''       # player's name initially
    main_menu(game)

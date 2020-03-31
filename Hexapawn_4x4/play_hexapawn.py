from dlgo import minimax
from dlgo import hexapawn

from six.moves import input

COL_NAMES = 'ABCD'


def print_board(board):
    print('   A   B   C   D')
    for row in (1, 2, 3, 4):
        pieces = []
        for col in (1, 2, 3, 4):
            piece = board.get(hexapawn.Point(row, col))
            if piece == hexapawn.Player.x:
                pieces.append('X')
            elif piece == hexapawn.Player.o:
                pieces.append('O')
            else:
                pieces.append(' ')
        print('%d  %s' % (row, ' | '.join(pieces)))
    print()


def point_from_coords(text):
    col_name = text[2]  
    row = int(text[3])
    return hexapawn.Point(row, COL_NAMES.index(col_name) + 1)


def main():
    game = hexapawn.GameState.new_game()

    human_player = hexapawn.Player.x
    # bot_player = hexapawn.Player.o

    bot = minimax.MinimaxAgent()

    while not game.is_over():
        print_board(game.board)
        if game.next_player == human_player:
            human_move = input('-- ')
            #get the starting position, the location of the piece the player selected to move
            start = hexapawn.Point(int(human_move[1]), COL_NAMES.index(human_move[0])+1)
            #get the end position, the location the player wants to move to.
            end = hexapawn.Point(int(human_move[3]), COL_NAMES.index(human_move[2])+1)
            move = hexapawn.Move(start, end)
            print()
        else:
            move = bot.select_move(game)
        
        #apply move only if the move is valid
        if(game.is_valid_move(move)):
            game = game.apply_move(move)

    print_board(game.board)
    winner = game.winner()
    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()

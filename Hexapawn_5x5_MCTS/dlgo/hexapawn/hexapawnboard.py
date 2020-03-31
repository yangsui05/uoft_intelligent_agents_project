import copy

from dlgo.hexapawn.hexapawntypes import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]


class IllegalMoveError(Exception):
    pass


BOARD_SIZE = 5
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))


class Board:
    def __init__(self):
        self._grid = {}

    def remove(self, player, point):
        #clear the player from the specified point
        assert self._grid.get(point) is player
        self._grid[point] = None
        
    def place(self, player, point):
        assert self.is_on_grid(point)
        #assert self._grid.get(point) is None
        self._grid[point] = player

    @staticmethod
    def is_on_grid(point):
        return 1 <= point.row <= BOARD_SIZE and \
            1 <= point.col <= BOARD_SIZE

    def get(self, point):
        """Return the content of a point on the board.

        Returns None if the point is empty, or a Player if there is a
        stone on that point.
        """
        return self._grid.get(point)


class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class GameState:
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move

    def apply_move(self, move):
        """Return the new GameState after applying the move."""
        next_board = copy.deepcopy(self.board)
        next_board.remove(self.next_player, move.start)
        next_board.place(self.next_player, move.end)
        return GameState(next_board, self.next_player.other, move)

    @classmethod
    def new_game(cls):
        board = Board()
        #place initial pawns on the board
        for col in COLS:
            board.place(Player.x, Point(BOARD_SIZE,col))
            board.place(Player.o, Point(1,col))
        return GameState(board, Player.x, None)

    def is_valid_move(self, move):
        #check that the move is within the board boundaries
        if(self.board.is_on_grid(move.start) and self.board.is_on_grid(move.end)):
            #if player x is on the starting point.
            if(self.board.get(move.start) == Player.x and move.start.row - move.end.row == 1):
                #check if the move is to advance forward and that there is an empty space to advance into
                if(move.start.col == move.end.col and self.board.get(move.end) is None):
                    return True
                elif(move.start.col - move.end.col == 1 and self.board.get(move.end) == Player.o):
                    return True
                elif(move.end.col - move.start.col == 1 and self.board.get(move.end) == Player.o):
                    return True
                else:
                    return False                  
            elif(self.board.get(move.start) == Player.o and move.end.row - move.start.row == 1):
                #check if the move is to advance forward and that there is an empty space to advance into
                if(move.start.col == move.end.col and self.board.get(move.end) is None):
                    return True
                elif(move.start.col - move.end.col == 1 and self.board.get(move.end) == Player.x):
                    return True
                elif(move.end.col - move.start.col == 1 and self.board.get(move.end) == Player.x):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def legal_moves(self):
        frontDir = 0    #variable to track which way is front. 
        if(self.next_player == Player.o):
            frontDir = 1
        else:
            frontDir = -1
        moves = []
        for row in ROWS:
            for col in COLS:
                if self.board.get(Point(row,col)) is self.next_player:
                    #iterate through the possible moves from this player position
                    for colOffset in (-1, 0, 1):
                        possibleMove = Move(Point(row,col), Point(row + frontDir, col + colOffset))
                        if(self.is_valid_move(possibleMove)):
                            moves.append(possibleMove)
        return moves

    def is_over(self):
        #check if any player has reached the opposite end of the board
        return (self._promoted(Player.x, 1) or self._promoted(Player.o, BOARD_SIZE) or len(self.legal_moves()) == 0)

    def winner(self):
        #check if any player has reached the opposite end of the board
        if(self._promoted(Player.x, 1)):
            return Player.x
        elif(self._promoted(Player.o, BOARD_SIZE)):
            return Player.o

        #check if player has run out of liberties
        if(self.legal_moves() == 0):
            return self.next_player.other()
        
        return None

    def _promoted(self, player, endRow):
        for col in COLS:
            if(self.board.get(Point(endRow, col)) == player):
                return True
        return False

    def get_next_player(self):
        return self.next_player
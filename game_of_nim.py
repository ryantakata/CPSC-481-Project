from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board=[3,1]):
        self.board = board
        moves = [(x, y) for x in range(len(board)) 
                 for y in range(1,board[x]+1)]
        self.initial = GameState(to_move='COMP', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        board = state.board.copy()
        board[move[0]] -= move[1]
        moves = [(x, y) for x in range(len(board)) 
                 for y in range(1,board[x]+1)]
        next = 'P1' if state.to_move == 'COMP' else 'COMP'
        utility = self.compute_utility(board, next)
        return GameState(to_move=next, 
                         utility=utility,
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        if player == 'COMP':
            return state.utility
        else:
            return -state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no objects left"""
        return len(state.moves) == 0

    def display(self, state):
        board = state.board
        print("board: ", board)

    def compute_utility(self, board, player):
        return 1 if self.terminal_test(GameState(player, 0, board, [])) else 0

if __name__ == "__main__":
    nim = GameOfNim(board=[0, 5, 3, 1]) # Creating the game instance
    #nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(nim.initial.board) # must be [0, 5, 3, 1]
    print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1,2) ))
    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first 
    print(utility)
    if (utility < 0):   
        print("P1 won the game")
    else:
        print("COMP won the game")
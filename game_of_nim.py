from games import *
from claude_helper import ClaudeHelper

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board=[3,1], use_claude=True):
        self.board = board
        moves = [(x, y) for x in range(len(board)) 
                 for y in range(1,board[x]+1)]
        self.initial = GameState(to_move='COMP', utility=0, board=board, moves=moves)
        self.claude = None
        if use_claude:
            try:
                self.claude = ClaudeHelper()
                # Test Claude API connection
                test_state = {"board": board, "to_move": "COMP", "moves": moves}
                self.claude.get_suggestions(test_state)
            except Exception as e:
                print(f"Claude API initialization failed: {str(e)}")
                self.claude = None

    def get_claude_suggestion(self, state):
        """Get a single move suggestion from Claude API"""
        if self.claude is None:
            return ("(0, 1)", "Claude API is not available")
            
        try:
            game_state = {
                "board": state.board,
                "to_move": state.to_move,
                "moves": state.moves
            }
            return self.claude.get_suggestions(game_state)
        except Exception as e:
            print(f"Error getting Claude suggestion: {str(e)}")
            return ("(0, 1)", f"Claude API error: {str(e)}")

    def get_eval_suggestion(self, state):
        """Get a move suggestion from evaluation function using alpha-beta pruning"""
        move = alpha_beta_search(state, self)
        heuristic = get_heuristic(state, move)
        board = state.board.copy()
        board[move[0]] -= move[1]

        return (str(move), f"Taking {move[1]} objects from row {move[0]} will reslt in a nim sum of {heuristic} and a board state of {board}.")

    def display_suggestions(self, claude_suggestion, eval_suggestion):
        """Display both Claude's and evaluation function's suggestions"""
        print("\nMove suggestions:")
        
        print("\nOption 1 (Claude's suggestion):")
        print(f"Move: {claude_suggestion[0]}")
        print(f"Explanation: {claude_suggestion[1]}")
        
        print("\nOption 2 (Evaluation function):")
        print(f"Move: {eval_suggestion[0]}")
        print(f"Explanation: {eval_suggestion[1]}")
        
        print("\nOption 3 (Enter your own move)")

    def get_user_choice(self, claude_suggestion, eval_suggestion, state):
        """Get user's choice between suggestions or their own move"""
        while True:
            choice = input("\nChoose an option (1, 2, or 3): ").strip()
            
            if choice == '1':
                return eval(claude_suggestion[0])
            elif choice == '2':
                return eval(eval_suggestion[0])
            elif choice == '3':
                return self.get_custom_move(state)
            print("Invalid choice. Please enter 1, 2, or 3.")

    def get_custom_move(self, state):
        """Get a custom move from the user"""
        while True:
            try:
                print("\nAvailable moves:", state.moves)
                move_str = input("Enter your move in format (row, number_of_objects): ")
                move = eval(move_str)
                
                # Validate the move
                if not isinstance(move, tuple) or len(move) != 2:
                    print("Move must be a tuple of two numbers")
                    continue
                    
                row, num = move
                if not isinstance(row, int) or not isinstance(num, int):
                    print("Row and number of objects must be integers")
                    continue
                    
                if row < 0 or row >= len(state.board):
                    print(f"Row must be between 0 and {len(state.board)-1}")
                    continue
                    
                if num < 1 or num > state.board[row]:
                    print(f"Number of objects must be between 1 and {state.board[row]}")
                    continue
                    
                return move
                
            except (SyntaxError, NameError):
                print("Invalid input format. Please enter in format (row, number_of_objects)")
            except Exception as e:
                print(f"Error: {str(e)}")

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
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
        """Print the current board state"""
        board = state.board
        print("board: ", board)

    def compute_utility(self, board, player):
        """Compute the utility of a board state for a player"""
        return 1 if self.terminal_test(GameState(player, 0, board, [])) else 0

def query_player_with_claude(game, state):
    """Make a move by querying the user and showing both Claude's and evaluation function's suggestions"""
    print("\nCurrent state:")
    game.display(state)
    
    # Get suggestions from both sources
    claude_suggestion = game.get_claude_suggestion(state)
    eval_suggestion = game.get_eval_suggestion(state)
    
    # Display suggestions
    game.display_suggestions(claude_suggestion, eval_suggestion)
    
    # Let user choose a move
    move = game.get_user_choice(claude_suggestion, eval_suggestion, state)
    return move

def get_heuristic(state, move):
    board = state.board.copy()
    board[move[0]] -= move[1]
    print(board)
    result = 0
    for stack in board:
        result ^= int(stack)
    return result

if __name__ == "__main__":
    # Create game instance with initial board [0, 5, 3, 1]
    nim = GameOfNim(board=[0, 5, 3, 1])
    
    # Print initial state
    print(nim.initial.board)  # Should be [0, 5, 3, 1]
    print(nim.initial.moves)  # Should be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    
    # Test a move
    print(nim.result(nim.initial, (1,2)))
    
    # Play the game with computer first (using alpha-beta pruning) and human second (with both suggestions)
    utility = nim.play_game(alpha_beta_player, query_player_with_claude)
    print(utility)
    
    # Print game result
    if (utility < 0):   
        print("P1 won the game")
    else:
        print("COMP won the game")
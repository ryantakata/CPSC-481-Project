from claude_helper import ClaudeHelper
from game_of_nim import GameOfNim

def get_user_choice(suggestions):
    """Get user's choice of move from Claude's suggestions"""
    while True:
        print("\nChoose a move (enter number 1 or 2):")
        for i, (move, explanation) in enumerate(suggestions, 1):
            print(f"\nOption {i}:")
            print(f"Move: {move}")
            print(f"Explanation: {explanation}")
        
        choice = input("\nYour choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            return suggestions[int(choice) - 1][0]
        print("Invalid choice. Please enter 1 or 2.")

def main():
    # Initialize the game
    game = GameOfNim()
    print("Initial game state:")
    print(game.initial.board)  # Print the initial board state
    
    # Initialize Claude helper
    try:
        claude = ClaudeHelper()
        print("\nGetting move suggestions from Claude...")
        
        # Get current game state
        game_state = {
            "board": game.initial.board,
            "current_player": game.initial.to_move,
            "moves": game.initial.moves
        }
        
        # Get suggestions
        suggestions = claude.get_suggestions(game_state)
        
        # Let user choose a move
        chosen_move = get_user_choice(suggestions)
        print(f"\nYou chose: {chosen_move}")
        
        # Apply the chosen move
        new_state = game.result(game.initial, eval(chosen_move))
        print("\nNew game state:")
        print(new_state.board)
        
        # Compare the moves if user wants
        compare = input("\nDo you want to compare the moves? (y/n): ").lower()
        if compare == 'y':
            print("\nComparing the two suggestions:")
            comparison = claude.compare_moves(game_state, suggestions[0][0], suggestions[1][0])
            print(comparison)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure you have set up your API key correctly in api_key.txt")

if __name__ == "__main__":
    main() 
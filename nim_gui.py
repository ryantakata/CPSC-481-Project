import tkinter as tk
from tkinter import ttk, messagebox
from game_of_nim import GameOfNim
from games import GameState

class NimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game of Nim")
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # Set window size to half screen width and full screen height
        self.root.geometry(f"{screen_width//2}x{screen_height}")

        # Game mode selection
        self.mode_var = tk.StringVar(value="PvP")
        self.first_var = tk.StringVar(value="Player")
        mode_frame = ttk.LabelFrame(root, text="Game Mode", padding="10")
        mode_frame.grid(row=0, column=0, pady=5, padx=10, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="Player vs Player", variable=self.mode_var, value="PvP").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="Player vs AI", variable=self.mode_var, value="PvE").grid(row=0, column=1, sticky=tk.W)
        self.first_label = ttk.Label(mode_frame, text="Who goes first:")
        self.first_combo = ttk.Combobox(mode_frame, textvariable=self.first_var, state="readonly", values=["Player", "AI"])
        self.first_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.first_combo.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.first_label.grid_remove()
        self.first_combo.grid_remove()
        self.mode_var.trace_add('write', self.toggle_first_option)

        # Start and Restart buttons
        self.start_button = ttk.Button(mode_frame, text="Start", command=self.start_game)
        self.start_button.grid(row=2, column=0, pady=5)
        self.restart_button = ttk.Button(mode_frame, text="Restart", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.grid(row=2, column=1, pady=5)

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Game status
        self.status_label = ttk.Label(self.main_frame, text="Game Status: Player 0's turn")
        self.status_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Piles display
        self.piles_frame = ttk.LabelFrame(self.main_frame, text="Piles", padding="5")
        self.piles_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.pile_labels = []
        for i in range(3):
            label = ttk.Label(self.piles_frame, text=f"Pile {i}: 0 objects")
            label.grid(row=i, column=0, padx=5, pady=5)
            self.pile_labels.append(label)

        # Move selection
        self.move_frame = ttk.LabelFrame(self.main_frame, text="Make a Move", padding="5")
        self.move_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Label(self.move_frame, text="Select Pile:").grid(row=0, column=0, padx=5)
        self.pile_var = tk.StringVar()
        self.pile_combo = ttk.Combobox(self.move_frame, textvariable=self.pile_var, state="readonly")
        self.pile_combo['values'] = [i for i in range(3)]
        self.pile_combo.grid(row=0, column=1, padx=5)
        ttk.Label(self.move_frame, text="Objects to remove:").grid(row=1, column=0, padx=5)
        self.objects_var = tk.StringVar()
        self.objects_entry = ttk.Entry(self.move_frame, textvariable=self.objects_var)
        self.objects_entry.grid(row=1, column=1, padx=5)
        self.move_button = ttk.Button(self.move_frame, text="Make Move", command=self.make_move, state=tk.DISABLED)
        self.move_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Suggestions
        self.suggestions_frame = ttk.LabelFrame(self.main_frame, text="Game Suggestions", padding="5")
        self.suggestions_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.suggestions_text = tk.Text(self.suggestions_frame, height=12, width=70, font=("Consolas", 14))
        self.suggestions_text.grid(row=0, column=0, padx=5, pady=5)
        self.suggestions_text.config(state=tk.DISABLED)
        
        # Add compare moves button
        self.compare_button = ttk.Button(self.suggestions_frame, text="Compare Moves", command=self.compare_moves, state=tk.DISABLED)
        self.compare_button.grid(row=1, column=0, pady=5)
        
        self.suggestions_button = ttk.Button(self.suggestions_frame, text="Get Suggestions", command=self.get_suggestions, state=tk.DISABLED)
        self.suggestions_button.grid(row=2, column=0, pady=5)

        # Game state
        self.game = None
        self.current_state = None
        self.claude_available = False
        self.is_ai_turn = False

    def toggle_first_option(self, *args):
        if self.mode_var.get() == "PvE":
            self.first_label.grid()
            self.first_combo.grid()
        else:
            self.first_label.grid_remove()
            self.first_combo.grid_remove()

    def start_game(self):
        # check Claude API
        try:
            from claude_helper import ClaudeHelper
            test_claude = ClaudeHelper()
            test_claude.get_suggestions({"board": [3, 4, 5], "to_move": "P1"})
            self.claude_available = True
        except Exception as e:
            print(f"Claude API not available: {str(e)}")
            self.claude_available = False
            messagebox.showwarning("Warning", "Claude API is not available. Suggestions will be limited to evaluation function only.")
        self.setup_game()
        self.move_button.config(state=tk.NORMAL)
        self.suggestions_button.config(state=tk.NORMAL)
        self.compare_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        # Clear suggestions box 
        self.suggestions_text.config(state=tk.NORMAL)
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.config(state=tk.DISABLED)

    def restart_game(self):
        self.setup_game()
        self.move_button.config(state=tk.NORMAL)
        self.suggestions_button.config(state=tk.NORMAL)
        # Clear suggestions box when restart game
        self.suggestions_text.config(state=tk.NORMAL)
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

    def setup_game(self):
        self.game = GameOfNim(board=[3, 4, 5], use_claude=self.claude_available)
        moves = [(x, y) for x in range(3) for y in range(1, [3, 4, 5][x]+1)]
        if self.mode_var.get() == "PvE":
            if self.first_var.get() == "AI":
                self.current_state = GameState(to_move='COMP', utility=0, board=[3, 4, 5], moves=moves)
            else:
                self.current_state = GameState(to_move='P1', utility=0, board=[3, 4, 5], moves=moves)
        else:
            self.current_state = GameState(to_move='P1', utility=0, board=[3, 4, 5], moves=moves)
        self.update_ui()
        self.root.after(100, self.after_update)

    def update_ui(self):
        for i in range(3):
            self.pile_labels[i].config(text=f"Pile {i}: {self.current_state.board[i]} objects")
        if self.game.terminal_test(self.current_state):
            winner = "Player 0" if self.current_state.to_move == 'COMP' else "Player 1"
            self.status_label.config(text=f"Game Over! {winner} wins!")
            self.move_button.config(state=tk.DISABLED)
        else:
            if self.mode_var.get() == "PvE":
                if self.current_state.to_move == 'COMP':
                    self.status_label.config(text="Game Status: AI's turn")
                else:
                    self.status_label.config(text="Game Status: Player's turn")
            else:
                current_player = "Player 0" if self.current_state.to_move == 'COMP' else "Player 1"
                self.status_label.config(text=f"Game Status: {current_player}'s turn")
            self.move_button.config(state=tk.NORMAL)

    def after_update(self):
        if self.game and self.mode_var.get() == "PvE" and not self.game.terminal_test(self.current_state):
            if self.current_state.to_move == 'COMP':
                self.root.after(700, self.ai_move)

    def make_move(self):
        try:
            pile = int(self.pile_var.get())
            objects = int(self.objects_var.get())
            if not (0 <= pile < len(self.current_state.board)):
                messagebox.showerror("Error", "Invalid pile selection")
                return
            if not (1 <= objects <= self.current_state.board[pile]):
                messagebox.showerror("Error", "Invalid number of objects")
                return
            move = (pile, objects)
            if move not in self.current_state.moves:
                messagebox.showerror("Error", "Invalid move")
                return
            self.current_state = self.game.result(self.current_state, move)
            self.update_ui()
            self.objects_var.set("")
            self.after_update()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def ai_move(self):
        move, _ = self.game.get_eval_suggestion(self.current_state)
        move = eval(move)
        self.current_state = self.game.result(self.current_state, move)
        self.update_ui()
        self.after_update()

    def get_suggestions(self):
        try:
            print(f"DEBUG: claude_available = {self.claude_available}, mode = {self.mode_var.get()}")
            print(f"DEBUG: current_state board = {self.current_state.board}, to_move = {self.current_state.to_move}, moves = {self.current_state.moves}")
            suggestions_text = ""
            if self.claude_available:
                try:
                    claude_suggestion = self.game.get_claude_suggestion(self.current_state)
                    suggestions_text += "Claude's Suggestion:\n"
                    suggestions_text += f"Move: {claude_suggestion[0]}\n"
                    suggestions_text += f"Explanation: {claude_suggestion[1]}\n\n"
                except Exception as e:
                    suggestions_text += "Claude's Suggestion:\n"
                    suggestions_text += f"Error: {str(e)}\n\n"
            eval_suggestion = self.game.get_eval_suggestion(self.current_state)
            suggestions_text += "Evaluation Function Suggestion:\n"
            suggestions_text += f"Move: {eval_suggestion[0]}\n"
            suggestions_text += f"Explanation: {eval_suggestion[1]}"
            self.suggestions_text.config(state=tk.NORMAL)
            self.suggestions_text.delete(1.0, tk.END)
            self.suggestions_text.insert(tk.END, suggestions_text)
            self.suggestions_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get suggestions: {str(e)}")

    def compare_moves(self):
        try:
            if not self.claude_available:
                messagebox.showwarning("Warning", "Claude API is not available. Cannot compare moves.")
                return
                
            # Get both suggestions
            claude_suggestion = self.game.get_claude_suggestion(self.current_state)
            eval_suggestion = self.game.get_eval_suggestion(self.current_state)
            
            # Get game state for comparison
            game_state = {
                "board": self.current_state.board,
                "to_move": self.current_state.to_move,
                "moves": self.current_state.moves
            }
            
            # Get comparison from Claude
            comparison = self.game.claude.compare_moves(game_state, claude_suggestion[0], eval_suggestion[0])
            
            # Display comparison
            self.suggestions_text.config(state=tk.NORMAL)
            self.suggestions_text.delete(1.0, tk.END)
            self.suggestions_text.insert(tk.END, "Move Comparison:\n\n")
            self.suggestions_text.insert(tk.END, comparison)
            self.suggestions_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare moves: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NimGUI(root)
    root.mainloop() 
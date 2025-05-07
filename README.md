# Game of Nim with Claude AI Integration

A modern implementation of the classic Game of Nim with advanced AI capabilities powered by Claude, providing intelligent move suggestions, strategic analysis, and interactive learning.

## Features

### Game Mechanics
- Full implementation of the classic Game of Nim
- Multiple board configurations
- Player vs Player and Player vs AI modes
- Interactive GUI interface
- Terminal-based playing option

### AI Integration
- **Claude API Integration**: Get expert move suggestions from Claude AI
- **Alpha-Beta Pruning AI**: Built-in AI player using minimax algorithm with alpha-beta pruning
- **Move Comparisons**: Compare different strategies with detailed analysis from Claude
- **Strategic Explanations**: Receive expert explanations for suggested moves
- **Fallback Mechanisms**: Graceful degradation when Claude API is unavailable

### User Experience
- **GUI Mode**: Attractive and intuitive graphical interface
- **Command Line Mode**: Quick and efficient terminal-based play
- **Suggestion System**: Request help at any point during gameplay
- **Move Comparison Tool**: Understand the strategic implications of different moves
- **Multi-platform**: Runs on Windows, macOS, and Linux

## Requirements

- Python 3.7+
- Anthropic API key (for Claude integration)
- Required Python packages:
  ```
  anthropic>=0.18.1
  numpy>=1.21.0
  tkinter (included with most Python installations)
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ryantakata/CPSC-481-Project
   cd game-of-nim
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a file named `api_key.txt` in the project root directory and add your Anthropic API key.


## Usage

### GUI Mode

Start the game with the graphical interface:

```bash
python nim_gui.py
```

The GUI provides:
- Game mode selection (Player vs Player or Player vs AI)
- First player selection
- Visual representation of piles
- Easy move selection
- Suggestion and comparison buttons
- Game status display

### Terminal Mode

Play the game in the terminal:

```bash
python game_of_nim.py
```

When playing in terminal mode, you'll have these options for each move:
1. Use Claude's suggestion
2. Use the evaluation function's suggestion
3. Enter your own move

### Testing Claude Integration

Test the Claude API integration separately:

```bash
python test_claude.py
```

## Playing with AI

### Setting Up the AI

This project features two different AI systems working together:

1. **Evaluation Function AI (Built-in)**: 
   - Uses alpha-beta pruning minimax algorithm 
   - Always available, no external dependencies
   - Functions as a fallback if Claude is unavailable
   - Implemented in `games.py` as `alpha_beta_player`

2. **Claude AI (API-based)**:
   - Powered by Anthropic's Claude API
   - Provides expert-level move suggestions and analysis
   - Requires API key in `api_key.txt`
   - Implemented in `claude_helper.py`

The integration between these systems happens in `game_of_nim.py` in the `GameOfNim` class, which can use both AIs together or fall back to just the evaluation function.

### AI Modes

#### Playing Against AI

1. In GUI mode, select "Player vs AI" and choose who goes first
2. The AI opponent uses the alpha-beta pruning algorithm by default
3. The difficulty is challenging as the AI uses optimal strategy

#### Getting AI Suggestions

1. During gameplay, click "Get Suggestions" to receive move recommendations
2. The system will provide two suggestions:
   - Claude's recommendation with explanation (if available)
   - Evaluation function's recommendation
3. You can then implement either suggestion or make your own move

#### Comparing AI Strategies

1. Click "Compare Moves" to see a detailed analysis
2. Claude will analyze both its own suggestion and the evaluation function's suggestion
3. The comparison includes immediate impact, strategic implications, and a recommendation

### Customizing AI Difficulty

You can adjust the AI difficulty by modifying the evaluation depth in `games.py`:

```python
# In game_of_nim.py
# Change the alpha_beta_cutoff_search depth parameter (default is 4)
# Lower numbers make the AI easier, higher numbers make it harder
move = alpha_beta_cutoff_search(state, game, d=2)  # Easier AI
```

## How It Works

### Game of Nim Rules
- The game starts with several piles of objects
- Players take turns removing objects
- On each turn, a player must remove at least one object from a single pile
- The player who takes the last object wins

### Claude Integration
The project uses the Anthropic API to get strategic insights from Claude:

1. **Move Suggestions**: Claude analyzes the game state and suggests optimal moves with explanations
2. **Move Comparisons**: Claude compares different possible moves and provides detailed analysis
3. **Strategic Insights**: Claude offers expert-level game theory explanations

### Error Handling
The system is designed to gracefully handle API issues:
- Tests API connectivity during initialization
- Falls back to evaluation function when Claude is unavailable
- Provides meaningful error messages

## Project Structure

- `claude_helper.py`: Claude API integration class
- `game_of_nim.py`: Core game implementation and logic
- `nim_gui.py`: Graphical user interface for the game
- `games.py`: Base game framework and AI algorithms
- `utils.py`: Utility functions
- `test_claude.py`: Test script for Claude integration
- `requirements.txt`: Project dependencies
- `api_key.txt`: Your Anthropic API key (not included, must be created)

## Extending the Project

### Custom Board Configurations
Modify the initial board state in `game_of_nim.py`:

```python
nim = GameOfNim(board=[3, 4, 5, 6])  # Create a game with 4 piles
```

### Custom Claude Prompts
Modify the prompts in `claude_helper.py` to change how Claude analyzes and responds.

### Additional AI Players
Implement new AI algorithms by creating new player functions in `games.py`.

## Troubleshooting

### API Key Issues
- Ensure your API key is valid and has sufficient credits
- Check that the `api_key.txt` file is in the correct location
- Verify that the key starts with `sk-ant-api`

### Connection Problems
- Check your internet connection
- Verify that your firewall allows outbound connections to the Anthropic API
- Review the console output for specific error messages

### GUI Issues
- Ensure Tkinter is properly installed
- On Linux, you may need to install Tkinter separately: `sudo apt-get install python3-tk`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Anthropic for the Claude API
- The Game of Nim for being an excellent example of game theory
- AIMA Python for the game framework inspiration
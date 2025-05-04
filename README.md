# Game of Nim with AI and Claude Integration

This project implements the Game of Nim with AI players and Claude API integration for move suggestions and analysis.

## Features

- Classic Game of Nim implementation
- AI player using alpha-beta pruning
- Claude API integration for move suggestions
- Evaluation function suggestions
- Custom move input option
- Move comparison and analysis

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Claude API:
   - Get your API key from [Anthropic Console](https://console.anthropic.com/)
   - Add your API key to `api_key.txt`

## How to Play

Run the game:
```bash
python game_of_nim.py
```

### Game Rules
- The game starts with several piles of objects
- Players take turns removing objects
- On each turn, a player must remove at least one object
- All objects must be taken from the same pile
- The player who takes the last object wins

### Move Options
When it's your turn, you have three options:
1. Use Claude's suggestion
2. Use the evaluation function's suggestion
3. Enter your own move

### Custom Move Format
When entering your own move, use the format:
```
(row, number_of_objects)
```
Example: `(1, 2)` means take 2 objects from row 1

## Project Structure

- `game_of_nim.py`: Main game implementation
- `games.py`: Core game framework and AI algorithms
- `claude_helper.py`: Claude API integration
- `utils.py`: Utility functions
- `api_key.txt`: Claude API key configuration

## Dependencies

- anthropic>=0.18.1
- numpy>=1.21.0
- pytest>=7.0.0

## Development

To modify or extend the project:

1. Game Logic: Edit `game_of_nim.py`
2. AI Algorithms: Edit `games.py`
3. Claude Integration: Edit `claude_helper.py`
4. GUI Window: Edit `nim_gui.py`

## Testing

Run tests:
```bash
python -m pytest
```

## License

This project is open source and available under the MIT License.
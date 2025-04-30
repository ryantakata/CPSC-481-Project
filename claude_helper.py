import os
import anthropic
from typing import List, Tuple
import json

class ClaudeHelper:
    def __init__(self):
        try:
            print("Initializing ClaudeHelper...")
            # Read API key from file
            with open('api_key.txt', 'r') as f:
                self.api_key = f.read().strip()
            print(f"API key read: {self.api_key[:10]}...")
            
            # Validate API key
            if not self.api_key:
                raise ValueError("API key is empty")
            if self.api_key == "your_api_key_here":
                raise ValueError("Please replace 'your_api_key_here' with your actual Claude API key")
            if not self.api_key.startswith("sk-ant-api"):
                raise ValueError("Invalid API key format")
                
            # Initialize client
            print("Initializing Anthropic client...")
            self.client = anthropic.Anthropic(api_key=self.api_key)
            print("Anthropic client initialized successfully")
            
            # Test connection
            print("Testing API connection...")
            try:
                response = self.client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1,
                    messages=[{"role": "user", "content": "test"}]
                )
                print("API connection test successful")
            except Exception as e:
                print(f"API connection test failed: {str(e)}")
                raise Exception(f"Failed to connect to Claude API: {str(e)}")
                
        except FileNotFoundError:
            print("api_key.txt not found")
            raise FileNotFoundError("api_key.txt not found. Please create it with your API key.")
        except Exception as e:
            print(f"Error in ClaudeHelper initialization: {str(e)}")
            raise Exception(f"Error initializing Claude API: {str(e)}")
    
    def get_suggestions(self, game_state: dict) -> Tuple[str, str]:
        """
        Get a single move suggestion from Claude API
        Args:
            game_state: Current state of the game
        Returns:
            Tuple of (move_description, explanation)
        """
        if not isinstance(game_state, dict):
            raise ValueError("game_state must be a dictionary")
            
        try:
            print("Preparing prompt for Claude API...")
            prompt = f"""
            You are an expert game player playing the Game of Nim. Given the following game state:
            {json.dumps(game_state, indent=2)}
            
            Please suggest one possible move. The move must be in the format of a tuple (row, number_of_objects).
            For example, if you want to take 2 objects from row 1, the move should be (1, 2).
            
            For the move:
            1. First, provide the move in the exact format: (row, number_of_objects)
            2. Then explain why this move would be good
            
            Format your response exactly as:
            Move: (row, number_of_objects)
            Explanation: [your explanation]
            
            Remember:
            - The move must be a valid tuple
            - The row must be a valid index in the board
            - The number_of_objects must be between 1 and the number of objects in that row
            """
            
            print("Sending request to Claude API...")
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            print("Received response from Claude API")
            
            # Parse the response to extract move and explanation
            move = None
            explanation = None
            
            for line in response.content[0].text.split('\n'):
                if line.startswith('Move:'):
                    move = line.split(': ')[1].strip()
                elif line.startswith('Explanation:'):
                    explanation = line.split(': ')[1].strip()
            
            if move and explanation:
                print(f"Successfully parsed response: Move={move}, Explanation={explanation}")
                return (move, explanation)
            else:
                print("Failed to parse Claude's response")
                raise Exception("Could not parse Claude's response")
                
        except Exception as e:
            print(f"Error in get_suggestions: {str(e)}")
            raise Exception(f"Error getting suggestions from Claude API: {str(e)}")
    
    def compare_moves(self, game_state: dict, move1: str, move2: str) -> str:
        """
        Compare two moves and provide analysis
        Args:
            game_state: Current state of the game
            move1: First move to compare
            move2: Second move to compare
        Returns:
            Detailed comparison analysis
        """
        if not isinstance(game_state, dict):
            raise ValueError("game_state must be a dictionary")
        if not isinstance(move1, str) or not isinstance(move2, str):
            raise ValueError("moves must be strings")
            
        try:
            prompt = f"""
            You are an expert game analyst. Given the following game state:
            {json.dumps(game_state, indent=2)}
            
            Compare these two moves:
            Move 1: {move1}
            Move 2: {move2}
            
            Analyze:
            1. The immediate impact of each move
            2. The strategic implications
            3. Which move you would recommend and why
            
            Provide a detailed comparison.
            """
            
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Error comparing moves with Claude API: {str(e)}") 
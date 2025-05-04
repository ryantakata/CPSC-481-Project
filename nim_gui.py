import pygame
import textwrap
import ast
from games import alpha_beta_search
from game_of_nim import GameOfNim

pygame.init()

# Game Window
WIDTH, HEIGHT = 1280, 720
FONT = pygame.font.SysFont('arial', 24)
SMALL_FONT = pygame.font.SysFont(None, 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Nim")

# Colors
WHITE = (30,65,31)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (236, 40, 50)

# Used for drawing stacks
current_state = None

# Creates the nim sticks
def draw_sticks(board):
    screen.fill(WHITE)
    stick_width = WIDTH // len(board)
    for i, count in enumerate(board):
        x = i * stick_width + stick_width // 2

        # Draws Sticks
        for j in range(count):
            y = HEIGHT - 50 - j * 25
            pygame.draw.rect(screen, GRAY, (x-10, y, 20, 20))
    
        # Label each row
        label = f"{i}"
        label_surf = FONT.render(label, True, BLACK)
        label_x = x-label_surf.get_width()//2
        label_y = HEIGHT - 30
        screen.blit(label_surf, (label_x, label_y))

    pygame.display.flip()

def draw_buttons(suggestions):
    global current_state
    buttons = []
    screen.fill(WHITE)

    # Draw sticks below the buttons
    draw_sticks(current_state.board)

    title = FONT.render("Choose a move:", True, RED)
    screen.blit(title, (WIDTH//2 - title.get_width() // 2, 50))

    # Button formatting
    button_width = 220
    button_height = 60
    spacing = 40
    total_width = 3 * button_width + 2 * spacing
    start_x = (WIDTH - total_width) // 2
    y = 150

    # Button, text box, and label creation
    for i, (move, explanation) in enumerate(suggestions):
        # Uncomment this if statement and indent everything until line 120 to disregard Custom button.
        # if i < len(suggestions)-1: 

        rect = pygame.Rect(start_x + i * (button_width + spacing), y, button_width, button_height)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Button Label
        if isinstance(move, tuple):
            label = explanation
        else:
            label = "Custom"
        
        label_surface = FONT.render(label, True, BLACK)
        label_x = rect.x + (button_width - label_surface.get_width())//2
        label_y = rect.y + 5
        screen.blit(label_surface, (label_x, label_y))

        # Move Label
        if isinstance(move, tuple):
            move_text = str(move[0])
        else:
            move_text = "Choose Move"
        
        move_label = SMALL_FONT.render(move_text, True, BLACK)
        move_x = rect.x + (button_width - move_label.get_width()) // 2
        move_y = label_y + 30
        screen.blit(move_label, (move_x, move_y))

        # Explanation Box Formatting
        if isinstance(move, tuple):
            text_box_y = move_y + 30
            if explanation == "Claude's Suggestion:":
                text_box_height = 350
            else:
                text_box_height = 50

            text_box_rect = pygame.Rect(rect.x, text_box_y, button_width, text_box_height)
            pygame.draw.rect(screen, (240, 240, 240), text_box_rect)
            pygame.draw.rect(screen, BLACK, text_box_rect, 1)
        
            max_chars = 28
            wrap_lines = textwrap.wrap(move[1], width=max_chars)

            line_y = text_box_y + 5
            for line in wrap_lines:
                if line_y + 18 > text_box_y + text_box_height:
                    break
                line_surface = SMALL_FONT.render(line, True, BLACK)
                screen.blit(line_surface, (rect.x + 5, line_y))
                line_y += 18

        buttons.append((rect, move, explanation))

    pygame.display.flip()
    return [(rect, move) for rect, move, _ in buttons]

def button_click(pos, board):
    x, y = pos
    for i in range(len(board)):
        stack_x = 100 + i*200
        if stack_x - 30 < x < stack_x + 30:
            return i
    return None

def show_winner(winner):
    screen.fill(WHITE)

    message = f"{winner} won!!"
    text_surf = pygame.font.SysFont(None, 60).render(message, True, (0, 128, 0))
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text_surf, text_rect)
    pygame.display.flip()

    pygame.time.wait(5000)

def main():
    game = GameOfNim(board=[3, 4, 5])
    state = game.initial
    custom_move = False
    selected_stack = None

    draw_sticks(state.board)

    running = True
    while running:
        draw_sticks(state.board)
        if game.terminal_test(state):
            winner="You" if state.to_move =="P1" else "AI"
            show_winner(winner)
            running = False
            continue

        if state.to_move == 'P1':
            if not custom_move:
                claude_suggestion = game.get_claude_suggestion(state)
                eval_suggestion = game.get_eval_suggestion(state)
                suggestions = GameOfNim.display_suggestions(state, claude_suggestion, eval_suggestion)
                print(suggestions)
                global current_state
                current_state = state
                buttons = draw_buttons(suggestions)

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            for rect, move in buttons:
                                if rect.collidepoint(event.pos):
                                    if move == "Custom":
                                        custom_move = True
                                        waiting = False
                                    else:
                                        nums = ast.literal_eval(move[0])
                                        state = game.result(state, nums)
                                        waiting = False
            else:
                # Custom Move
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    stack = button_click(event.pos, state.board)
                    if stack is not None:
                        selected_stack = stack
                        print(f"Selected stack {stack}. Press number key to remove objects.")
                elif event.type == pygame.KEYDOWN and selected_stack is not None:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        amount = event.key - pygame.K_0
                        move = (selected_stack, amount)
                        if move in state.moves:
                            state = game.result(state, nums)
                            custom_move = False
                            break
                        else:
                            print("Invalid move")
        else:
            # pygame.time.wait(100)
            move = alpha_beta_search(state, game)
            print(f"AI chooses {move}")
            state = game.result(state, move)

    pygame.quit()

if __name__ == "__main__":
    main()
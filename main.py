
# Global variable for map size
map_size = 0
# Main file for program execution and functionality


# ROADMAP #1: Import necessary modules (random, os, sys, etc.)
import random  # For random mine placement and random start
import os      # For clearing the console
import sys     # For system exit if needed


# ROADMAP #2: Define constants for map size, number of mines, tile symbols, etc.
DIFFICULTY_SETTINGS = {
    "easy": {"size": 4, "mines": 8},
    "medium": {"size": 6, "mines": 15},
    "hard": {"size": 8, "mines": 24},
    "very hard": {"size": 10, "mines": 35}
}
map_size = 0
clear_tiles_revealed = 0

def select_difficulty():
    # Prompt the user to select a difficulty and return the corresponding settings.
    print("Select difficulty:")
    print("1. Easy (6x6)")
    print("2. Medium (8x8)")
    print("3. Hard (10x10)")
    print("4. Very Hard (12x12)")
    choice = input("Enter 1-4: ").strip()
    match choice:
        case "1":
            return DIFFICULTY_SETTINGS["easy"]
        case "2":
            return DIFFICULTY_SETTINGS["medium"]
        case "3":
            return DIFFICULTY_SETTINGS["hard"]
        case "4":
            return DIFFICULTY_SETTINGS["very hard"]
        case _:
            print("Invalid choice, defaulting to Easy.")
            return DIFFICULTY_SETTINGS["easy"]



class Tile:
    # Represents a single tile on the Minesweeper board.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.adjacent_mines = 0

def random_start(minefield):
    # Find a random clear tile with at least one clear neighbor to use as the starting tile.
    size = len(minefield)
    clear_candidates = []
    for x in range(size):
        for y in range(size):
            tile = minefield[x][y]
            if not tile.is_mine:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < size and 0 <= ny < size:
                            neighbor = minefield[nx][ny]
                            if not neighbor.is_mine:
                                clear_candidates.append((x, y))
                                break
                    else:
                        continue
                    break
    if clear_candidates:
        return random.choice(clear_candidates)
    else:
        for x in range(size):
            for y in range(size):
                if not minefield[x][y].is_mine:
                    return (x, y)
        return (0, 0)

def generate_minefield(difficulty):
    # Generate the minefield based on difficulty, place mines, and guarantee a clear starting tile.
    size = difficulty["size"]
    num_mines = difficulty["mines"]
    minefield = [[Tile(x, y) for y in range(size)] for x in range(size)]
    mines_placed = 0
    while mines_placed < num_mines:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if not minefield[x][y].is_mine:
            minefield[x][y].is_mine = True
            mines_placed += 1
    # Guarantee a random clear start with at least one clear neighbor
    start_x, start_y = random_start(minefield)
    minefield[start_x][start_y].is_mine = False
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = start_x + dx, start_y + dy
            if 0 <= nx < size and 0 <= ny < size:
                neighbors.append((nx, ny))
    random.shuffle(neighbors)
    for nx, ny in neighbors:
        minefield[nx][ny].is_mine = False
        break
    # Recalculate adjacent mines
    for x in range(size):
        for y in range(size):
            if minefield[x][y].is_mine:
                continue
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        if minefield[nx][ny].is_mine:
                            count += 1
            minefield[x][y].adjacent_mines = count
    return minefield, (start_x, start_y)


# ROADMAP #4: Implement a function to display the minefield in the terminal, showing revealed and unrevealed tiles.
#Refresh step 1: Clear Terminal
def Clear_console():
    # Clear the terminal screen for better display of the minefield.
    os.system('cls')

def refresh_minefield(minefield):
    # Display the current state of the minefield in the terminal.
    Clear_console()
    size = len(minefield)
    print("   " + " ".join(str(i+1) for i in range(size)))
    for idx, row in enumerate(minefield):
        print(chr(ord('a')+idx) + "  " + " ".join(
            'M' if t.is_mine and t.is_revealed else (str(t.adjacent_mines) if t.is_revealed else '#') for t in row))
    print("\n")

def check_tile(minefield, row, col):
    # Reveal the tile at (row, col). If it's a mine, end the game. If not, reveal and auto-reveal if needed.
    tile = minefield[row][col]
    if tile.is_mine:
        print("You hit a mine! Game over.")
        tile.is_revealed = True
        return False
    if tile.is_revealed:
        print("Tile already revealed.")
        return True
    tile.is_revealed = True
    global clear_tiles_revealed
    clear_tiles_revealed += 1
    if tile.adjacent_mines == 0:
        auto_reveal(minefield, row, col)
    return True

def auto_reveal(minefield, row, col):
    # Recursively reveal all connected empty tiles starting from (row, col).
    size = len(minefield)
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        tile = minefield[r][c]
        if tile.is_revealed or tile.is_mine:
            continue
        tile.is_revealed = True
        global clear_tiles_revealed
        clear_tiles_revealed += 1
        if tile.adjacent_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nr, nc = r + dx, c + dy
                    if 0 <= nr < size and 0 <= nc < size:
                        neighbor = minefield[nr][nc]
                        if not neighbor.is_revealed and not neighbor.is_mine:
                            stack.append((nr, nc))

# ROADMAP #5: Handle user input for coordinates (e.g., "a1", "b5"), including input validation and conversion to map indices.
def get_user_input():
    # Prompt the user for coordinates, validate, and convert to board indices.
    while True:
        user_input = input("Enter coordinates (e.g., a1, b5): ").strip().lower()
        if len(user_input) < 2 or len(user_input) > 3:
            print("Invalid input. Please enter coordinates in the format 'a1', 'b5', etc.")
            continue
        row = ord(user_input[0]) - ord('a')
        try:
            col = int(user_input[1:]) - 1
        except ValueError:
            print("Invalid input. Please enter coordinates in the format 'a1', 'b5', etc.")
            continue
        if row < 0 or row >= map_size or col < 0 or col >= map_size:
            print("Coordinates out of bounds. Please try again.")
            continue
        return row, col
# ROADMAP #6: Implement game logic for revealing tiles, checking for mines, and handling win/loss conditions.
def check_tile(minefield, row, col):
    tile = minefield[row][col]
    if tile.is_mine:
        print("You hit a mine! Game over.")
        tile.is_revealed = True
        return False  # Game over
    if tile.is_revealed:
        print("Tile already revealed.")
        return True
    tile.is_revealed = True
    global clear_tiles_revealed
    clear_tiles_revealed += 1
    if tile.adjacent_mines == 0:
        auto_reveal(minefield, row, col)
    return True

# ROADMAP #7: Track the number of clear tiles revealed by the user for scoring purposes.
clear_tiles_revealed = 0
# ROADMAP #8: On game completion (win or loss), prompt the user for their initials and calculate their score.
def user_initials_and_score():
    # Prompt the user for initials and display their score.
    initials = input("Enter your initials: ").strip().upper()
    score = clear_tiles_revealed
    print(f"Your score: {score}")
    return initials, score
# ROADMAP #9: Write the user's initials and score to scoreboard.txt.
def scoreboard(initials, score):
    # Append the user's initials and score to the scoreboard file.
    with open("scoreboard.txt", "a") as f:
        f.write(f"{initials}: {score}\n")
    print("Score saved to scoreboard.txt")

# ROADMAP #10: Implement a main game loop to tie all components together and restart or exit as needed.
def main():
    # Main game loop: handles setup, gameplay, win/loss, and replay logic.
    global clear_tiles_revealed, map_size

    # Get difficulty settings from user
    settings = select_difficulty()  # User selects difficulty
    map_size = settings["size"]
    num_mines = settings["mines"]
    # Generate the minefield and get a guaranteed clear starting tile
    minefield, (start_x, start_y) = generate_minefield(settings)
    print(f"Starting game with size {map_size}x{map_size} and {num_mines} mines.")
    game_over = False
    clear_tiles_revealed = 0

    # Reveal the random start tile and its area before the game loop
    check_tile(minefield, start_x, start_y)  # Ensures the player starts with a revealed area

    while not game_over:
        refresh_minefield(minefield)  # Show the current board state
        row_idx, col_idx = get_user_input()  # Get the user's move
        # Reveal the selected tile; if it's a mine, end the game
        if not check_tile(minefield, row_idx, col_idx):
            # Reveal all mines after loss
            for r in minefield:
                for t in r:
                    if t.is_mine:
                        t.is_revealed = True
            refresh_minefield(minefield)
            print("You hit a mine! Game over.")
            game_over = True
        else:
            # Check for win condition
            total_safe = map_size * map_size - num_mines
            if clear_tiles_revealed == total_safe:
                # Reveal all tiles after win
                for r in minefield:
                    for t in r:
                        t.is_revealed = True
                refresh_minefield(minefield)
                print("Congratulations! You cleared the minefield!")
                game_over = True
    # Prompt for initials and save score after game ends
    initials, score = user_initials_and_score()
    scoreboard(initials, score)
    # Ask the user if they want to play again
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again == 'y':
            main()  # Restart the game
            break
        elif again == 'n':
            print("Thanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")


# Entry point for the program
if __name__ == "__main__":
    main()  # Start the game



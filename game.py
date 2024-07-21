import pygame
import tkinter as tk
from tkinter import scrolledtext
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 40  # Size of each grid cell
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

class Player(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.update_position()

    def update_position(self):
        self.rect.x = self.grid_x * GRID_SIZE
        self.rect.y = self.grid_y * GRID_SIZE

    def move(self, dx, dy):
        new_x = max(0, min(GRID_WIDTH - 1, self.grid_x + dx))
        new_y = max(0, min(GRID_HEIGHT - 1, self.grid_y + dy))
        if (new_x, new_y) != (self.grid_x, self.grid_y):
            self.grid_x, self.grid_y = new_x, new_y
            self.update_position()
            return True
        return False

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Realmrite MVP")

        # Create Pygame frame
        self.frame = tk.Frame(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.frame.pack(side=tk.LEFT)
        self.embed = tk.Frame(self.frame, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.embed.pack()
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        # Create CLI frame
        self.cli_frame = tk.Frame(self.root, width=200, height=SCREEN_HEIGHT)
        self.cli_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.cli_text = scrolledtext.ScrolledText(self.cli_frame, wrap=tk.WORD, width=30, height=35)
        self.cli_text.pack()
        self.cli_entry = tk.Entry(self.cli_frame)
        self.cli_entry.pack()
        self.cli_entry.bind("<Return>", self.process_command)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Realmrite MVP")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = None
        self.all_sprites = pygame.sprite.Group()

        # Bind Tab key to switch focus
        self.root.bind("<Tab>", self.switch_focus)
        self.focus_on_pygame = True

        # Bind arrow keys
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)

        # Initial instructions
        self.update_cli_text("Welcome to Realmrite MVP!\n")
        self.update_cli_text("Use the arrow keys to move the player.\n")
        self.update_cli_text("Press Tab to switch focus between the game and the CLI.\n")
        self.update_cli_text("Enter commands in the CLI and press Enter.\n")

        self.state = "MENU"
        self.setup_menu()

    def setup_menu(self):
        button_width, button_height = 200, 50
        start_x = (SCREEN_WIDTH - button_width) // 2
        start_y = SCREEN_HEIGHT // 2 - 100

        self.menu_buttons = [
            Button(start_x, start_y, button_width, button_height, "New Game", (0, 255, 0), BLACK, self.start_new_game),
            Button(start_x, start_y + 60, button_width, button_height, "Continue", (0, 200, 0), BLACK, self.continue_game),
            Button(start_x, start_y + 120, button_width, button_height, "Settings", (0, 150, 0), BLACK, self.open_settings),
            Button(start_x, start_y + 180, button_width, button_height, "Exit", (255, 0, 0), BLACK, self.exit_game)
        ]

    def start_new_game(self):
        self.state = "PLAYING"
        self.player = Player(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.update_cli_text("Starting a new game...\n")

    def continue_game(self):
        self.update_cli_text("Continue game pressed. This feature is not implemented yet.\n")

    def open_settings(self):
        self.update_cli_text("Settings pressed. This feature is not implemented yet.\n")

    def exit_game(self):
        self.running = False
        self.update_cli_text("Exiting game...\n")

    def switch_focus(self, event):
        if self.focus_on_pygame:
            self.cli_entry.focus_set()
            self.update_cli_text("CLI input is now active. Type your command and press Enter.\n")
        else:
            self.focus_pygame_window()
            self.update_cli_text("Game window is now active. Use arrow keys to move.\n")
        self.focus_on_pygame = not self.focus_on_pygame
        return 'break'  # This prevents the default Tab behavior

    def focus_pygame_window(self):
        pygame.display.get_wm_info()
        self.embed.focus_set()

    def on_key_press(self, event):
        if self.focus_on_pygame and self.state == "PLAYING":
            dx, dy = 0, 0
            if event.keysym == 'Left':
                dx = -1
            elif event.keysym == 'Right':
                dx = 1
            elif event.keysym == 'Up':
                dy = -1
            elif event.keysym == 'Down':
                dy = 1
            
            if self.player.move(dx, dy):
                self.update_cli_text(f"Player moved {event.keysym}\n")
            else:
                self.update_cli_text(f"Cannot move {event.keysym}\n")

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            self.root.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == "MENU":
                for button in self.menu_buttons:
                    button.handle_event(event)
            elif self.state == "PLAYING":
                # Handle game events
                pass

    def update(self):
        if self.state == "PLAYING":
            self.all_sprites.update()

    def draw(self):
        self.screen.fill(WHITE)
        if self.state == "MENU":
            for button in self.menu_buttons:
                button.draw(self.screen)
        elif self.state == "PLAYING":
            self.draw_grid()
            self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    def process_command(self, event):
        command = self.cli_entry.get()
        self.cli_entry.delete(0, tk.END)
        self.update_cli_text(f"You entered: {command}\n")
        
        if command.lower() == "exit":
            self.exit_game()
        else:
            # Process other commands (for now, just print it)
            print(f"Command entered: {command}")

    def update_cli_text(self, text):
        self.cli_text.insert(tk.END, text)
        self.cli_text.see(tk.END)

# Main function
def main():
    root = tk.Tk()
    game = Game(root)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
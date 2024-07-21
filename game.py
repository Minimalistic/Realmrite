import pygame
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Game class
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
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.player)

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
        # Focus on the Pygame window to capture keyboard events
        pygame.display.get_wm_info()
        self.embed.focus_set()

    def on_key_press(self, event):
        if self.focus_on_pygame:
            if event.keysym == 'Left':
                self.player.rect.x -= self.player.speed
            elif event.keysym == 'Right':
                self.player.rect.x += self.player.speed
            elif event.keysym == 'Up':
                self.player.rect.y -= self.player.speed
            elif event.keysym == 'Down':
                self.player.rect.y += self.player.speed
            self.update_cli_text(f"Player moved {event.keysym}\n")

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

    def update(self):
        self.all_sprites.update(pygame.key.get_pressed())

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def process_command(self, event):
        command = self.cli_entry.get()
        self.cli_entry.delete(0, tk.END)
        self.update_cli_text(f"You entered: {command}\n")
        # Process the command (for now, just print it)
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
import socket
import threading
import pygame

# Client settings
HOST = '127.0.0.1'
PORT = 65432

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
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(color)
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
    def __init__(self, client_socket):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Realmrite MVP")
        self.clock = pygame.time.Clock()
        self.running = True
        self.client_socket = client_socket
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RED)
        self.other_players = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.all_sprites.update(keys)
        self.send_position()
        self.receive_positions()

    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def send_position(self):
        pos = f"{self.player.rect.x},{self.player.rect.y}"
        self.client_socket.sendall(pos.encode())

    def receive_positions(self):
        try:
            data = self.client_socket.recv(1024).decode()
            if data:
                positions = data.split(";")
                self.other_players.empty()
                for pos in positions:
                    if pos:
                        x, y = map(int, pos.split(","))
                        other_player = Player(x, y, BLUE)
                        self.other_players.add(other_player)
                self.all_sprites.add(self.other_players)
        except:
            pass

# Main function
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    game = Game(client_socket)
    game.run()
    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    main()
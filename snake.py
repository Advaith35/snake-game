import pygame
import sys
import random

# Pygame ni initialize cheyyi
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400  # Window anta peru, paniyaalu
GRID_SIZE = 20  # Okati grid cell size
FPS = 10  # Prati second lo frames

# Rangulu
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1  # Snake length
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]  # Position of snake
        self.direction = random.choice([0, 1, 2, 3])  # 0: up, 1: right, 2: down, 3: left
        self.color = GREEN  # Snake color

    def get_head_position(self):
        return self.positions[0]  # Head position of snake

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction if isinstance(self.direction, tuple) else (1, 0)

        new = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()  # Snake ni reset cheseyi if it collides with itself
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([0, 1, 2, 3])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
                         random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game if window is closed
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Change snake direction based on arrow key pressed
                if event.key == pygame.K_UP:
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.direction = (1, 0)

        snake.update()  # Update snake position
        if snake.get_head_position() == food.position:
            snake.length += 1  # Increase snake length when it eats food
            food.randomize_position()  # Generate new food position

        surface.fill(BLACK)  # Fill surface with black color
        snake.render(surface)  # Render snake on the surface
        food.render(surface)  # Render food on the surface
        screen.blit(surface, (0, 0))  # Blit surface onto the screen
        pygame.display.update()  # Update display
        clock.tick(FPS)  # Cap FPS

if __name__ == "__main__":
    main()

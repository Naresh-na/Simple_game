import random

import pygame
from pygame.locals import *
import time

size = 30
background_color = 110, 56, 66


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size*3
        self.y = size*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 32) * size
        self.y = random.randint(0, 25) * size


class Snake:     # Creating a Class name called Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.png").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def draw(self):
        self.parent_screen.fill(background_color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'up':
            self.y[0] -= size

        if self.direction == 'down':
            self.y[0] += size

        if self.direction == 'left':
            self.x[0] -= size

        if self.direction == 'right':
            self.x[0] += size

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((110, 56, 66))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True

            return False

    def dispaly_score(self):
        font = pygame.font.SysFont('Arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (225, 225, 225))
        self.surface.blit(score, (800, 10))

    def play(self):
        self.snake.walk()  # from calling the walk() method : Line 32
        self.apple.draw()
        self.dispaly_score()
        pygame.display.flip()

        # Snake colliding with apple.

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with snake.

        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

    def show_game_over(self):
        self.surface.fill(background_color)
        font = pygame.font.SysFont('Arial', 30)
        line1 = font.render(f"Game Over! Your Score is {self.snake.length}", True, (225, 225, 225))
        self.surface.blit(line1, (400, 300))
        line2 = font.render("To play again (Press Enter)", True, (225, 225, 225))
        self.surface.blit(line2, (400, 350))
        line3 = font.render("To exit (Press ESC)", True, (225, 225, 225))
        self.surface.blit(line3, (400, 400))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()   # from Line 15

                        if event.key == K_DOWN:
                            self.snake.move_down()  # from Line 18

                        if event.key == K_LEFT:
                            self.snake.move_left()   # from Line 21

                        if event.key == K_RIGHT:
                            self.snake.move_right()   # form Line 24

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == '__main__':
    game = Game()
    game.run()

import pygame
import time
import colorama
from src.runner import StateRunner
from src.variables import GameVars
from src.loader import get_gfx


class Game:
    def __init__(self) -> None:
        colorama.init(autoreset=True)
        pygame.display.set_caption('Set a caption')
        pygame.display.set_icon(get_gfx('default'))
        self.state_runner = StateRunner()
        self.pre_time = time.time()
        self.clock = pygame.time.Clock()
    
    def run(self) -> None:
        while True:
            self.clock.tick(GameVars.fps)
            dt = time.time() - self.pre_time
            self.pre_time = time.time()
            self.state_runner.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

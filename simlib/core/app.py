import pygame
from abc import ABC, abstractmethod

class Simulation(ABC):

    def setup(self):
        '''Initialize Simulation'''

    def handle_event(self, event: pygame.event.Event):
        '''Handles events'''

    @abstractmethod
    def update(self, dt: float):
        '''Advance the simulation by dt seconds. Called by App at a fixed rate, so dt is the same on every call. Must not draw anything.'''

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        '''Draw to screen'''

class App:
    def __init__(self, sim: Simulation, size=(800,600), title="Simulation", bg_color=(0,0,0), fps=60.0):
        '''Initialise App'''
        self.sim = sim
        self.size = size
        self.title = title
        self.fps = fps
        self.screen = None
        self.clock = None
        self.bg_color=bg_color

        

    def run(self):
        '''Initialise pygame and run main loop'''
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
        self.clock = pygame.Clock()
        self.sim.setup()
        self._running = True
        try:
            while self._running:
                dt = self.clock.tick(self.fps) / 1000
                self._handle_events()
                self.sim.update(dt)
                self.screen.fill(self.bg_color)
                self.sim.draw(self.screen)
                pygame.display.flip()
        finally:
            pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            else:
                self.sim.handle_event(event)

class CircleTest(Simulation):
    def setup(self):
        self.x = 400
    def update(self, dt):
        self.x += 10 * dt
    def draw(self, screen):
        pygame.draw.circle(screen, "red", (self.x, 300), 40)

if __name__ == "__main__":
    app = App(CircleTest())
    app.run()
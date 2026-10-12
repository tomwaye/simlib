from simlib.core.app import App, Simulation
import pygame

class CircleTest(Simulation):
    """Temporary demo: a circle moving right at 50 pixels per second."""

    def setup(self) -> None:
        self.x = 400
    def update(self, dt: float) -> None:
        self.x += 50 * dt
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", (self.x, 300), 40)

if __name__ == "__main__":
    app = App(CircleTest(), fps=60.0)
    app.run()
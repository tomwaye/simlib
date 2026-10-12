import pygame
from abc import ABC, abstractmethod
import simlib.core.timing as timing

class Simulation(ABC):
    """Base class for anything App can run.

    Subclass it and implement update and draw. Override setup and
    handle_event only if you need them.
    """

    def setup(self) -> None:
        """Prepare the simulation's initial state.

        Called once by App.run, after the window exists and before the
        first update. Does nothing by default.
        """

    def handle_event(self, event: pygame.event.Event) -> None:
        """React to a pygame event such as a mouse click or key press.

        Receives every event except quitting and App's reserved keys (see
        App). Does nothing by default.
        """

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance the simulation by dt seconds.

        Called by App at a fixed rate, so dt is the same on every call.
        Must not draw anything.
        """

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the current state onto screen.

        Called once per frame, including while paused. The screen has
        already been filled with the background colour. Must not change
        the simulation's state.
        """

class App:
    """Owns the window and main loop, and runs a Simulation.

    Updates the simulation at a fixed time step and draws it once per
    frame. The window title shows the measured frame rate.

    Reserved keys:
        Esc: quit.
        Space: pause or resume.
        F: toggle fullscreen.
        Right arrow: while paused, advance by one step. When not paused it
            is passed to the simulation.

    All other events are passed to Simulation.handle_event.
    """

    def __init__(
        self,
        sim: Simulation,
        size: tuple[int, int] = (800, 600),
        title: str = "Simulation",
        bg_color: tuple[int, int, int] = (0, 0, 0),
        fps: float = 60.0,
        step: float = 1 / 60,
    ) -> None:
        """Store settings. Does not open a window; call run for that.

        Args:
            sim: The simulation to run.
            size: Window size in pixels, as (width, height). Fullscreen
                scales this up without changing the size the simulation
                draws at.
            title: Window title.
            bg_color: RGB colour the screen is filled with before each draw.
            fps: Target frames per second. The loop runs no faster than
                this, but may run slower.
            step: Length of one simulation update, in seconds.
        """
        self.sim = sim
        self.size = size
        self.title = title
        self.fps = fps
        self.actual_fps = fps
        self.screen = None
        self.clock = None
        self.stepper = None
        self.bg_color=bg_color
        self.step = step
        self._running = True
        self._paused = False


    def run(self) -> None:
        """Open the window and run the main loop until the user quits.

        Calls sim.setup once, then each frame handles events, runs as many
        fixed-size updates as the elapsed time allows (none while paused),
        and draws. Pygame is shut down when the loop ends, even if the
        simulation raises an exception.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.SCALED)
        pygame.display.set_caption(self.title)
        self.clock = pygame.Clock()
        self.sim.setup()
        self.stepper = timing.FixedStep(self.step)
        self._caption_timer = 0.0
        self._running = True
        self._paused = False
        try:
            while self._running:
                dt = self.clock.tick(self.fps) / 1000
                self.actual_fps = self.clock.get_fps()
                self._handle_events()
                self._set_caption(0.5, dt)
                if not self._paused:
                    n = self.stepper.advance(dt)
                    for _ in range(n):
                        self.sim.update(self.stepper.step)
                self.screen.fill(self.bg_color)
                self.sim.draw(self.screen)
                pygame.display.flip()
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Process all pending events: quit, reserved keys, or pass to the sim."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_key(event)
            else:
                self.sim.handle_event(event)

    def _handle_key(self, event: pygame.event.Event) -> None:
        """Act on a reserved key, or pass any other key press to the sim."""
        if event.key == pygame.K_ESCAPE:
            self._running = False
        elif event.key == pygame.K_SPACE:
            self._paused = not self._paused
            self._update_caption()
        elif event.key == pygame.K_f:
            pygame.display.toggle_fullscreen()
        elif event.key == pygame.K_PERIOD:
            if self._paused:
                self.sim.update(self.step)
            else:
                self.sim.handle_event(event)
        else:
            self.sim.handle_event(event)

    def _set_caption(self, interval: float, dt: float) -> None:
        """Refresh the window title with the frame rate every interval seconds.

        Args:
            interval: Seconds between title updates.
            dt: Seconds since the last frame, added to the timer.
        """
        self._caption_timer += dt
        if self._caption_timer >= interval:
            self._update_caption()
            self._caption_timer = self._caption_timer - interval

    def _update_caption(self) -> None:
        """Set the window title now, showing the frame rate and pause state."""
        if not self._paused:
            pygame.display.set_caption(f"{self.title} | {int(self.actual_fps)} FPS")
        else:
            pygame.display.set_caption(f"{self.title} | {int(self.actual_fps)} FPS | PAUSED")


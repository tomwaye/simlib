import pygame
import pytest

from simlib.core.app import App, Simulation


class CountingSim(Simulation):
    """Test double: records what App does to it instead of simulating anything."""

    def __init__(self) -> None:
        self.dts: list[float] = []
        self.events: list[pygame.event.Event] = []

    def handle_event(self, event: pygame.event.Event) -> None:
        self.events.append(event)

    def update(self, dt: float) -> None:
        self.dts.append(dt)

    def draw(self, screen: pygame.Surface) -> None:
        pass


def key(k: int) -> pygame.event.Event:
    """Make a fake key press. Creating events does not need a window."""
    return pygame.event.Event(pygame.KEYDOWN, key=k)


@pytest.fixture
def app() -> App:
    return App(CountingSim(), step=1 / 120)


def test_simulation_without_update_and_draw_cannot_be_created():
    class Incomplete(Simulation):
        pass

    with pytest.raises(TypeError):
        Incomplete()


def test_creating_app_does_not_open_window():
    App(CountingSim())
    assert pygame.display.get_surface() is None


def test_space_pauses(app):
    app._handle_key(key(pygame.K_SPACE))
    assert app._paused


def test_space_twice_resumes(app):
    app._handle_key(key(pygame.K_SPACE))
    app._handle_key(key(pygame.K_SPACE))
    assert not app._paused


def test_escape_stops_running(app):
    app._handle_key(key(pygame.K_ESCAPE))
    assert not app._running


def test_step_key_while_paused_runs_one_update_of_step_length(app):
    app._paused = True
    app._handle_key(key(pygame.K_RIGHT))
    assert app.sim.dts == [1 / 120]


def test_step_key_while_running_is_passed_to_sim(app):
    app._handle_key(key(pygame.K_RIGHT))
    assert app.sim.dts == []
    assert [e.key for e in app.sim.events] == [pygame.K_RIGHT]


def test_unreserved_key_is_passed_to_sim(app):
    app._handle_key(key(pygame.K_a))
    assert [e.key for e in app.sim.events] == [pygame.K_a]


@pytest.mark.parametrize("reserved", [pygame.K_SPACE, pygame.K_ESCAPE])
def test_reserved_keys_are_not_passed_to_sim(app, reserved):
    app._handle_key(key(reserved))
    assert app.sim.events == []

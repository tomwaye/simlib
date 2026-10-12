# simlib

A reusable Python library for building 2D simulations, using NumPy and
[pygame-ce](https://pyga.me/).

You write a simulation's state, its `update` and its `draw`, and simlib
handles the window, main loop, timing, pause and fullscreen. The library is
being built up one component at a time, each one extracted from a working
simulation project such as boids or an ant colony.

> **Status:** early development. The application framework and fixed time
> step are done. See the [roadmap](#roadmap) for what comes next.

## Quick start

Requires Python 3.11 or later.

```bash
git clone https://github.com/tomwaye/simlib.git
cd simlib
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python examples/circle_test.py
```

## Writing a simulation

Subclass `Simulation`, implement `update` and `draw`, and pass an instance to
`App`:

```python
import pygame
from simlib.core.app import App, Simulation


class MovingCircle(Simulation):
    def setup(self) -> None:
        self.x = 100.0

    def update(self, dt: float) -> None:
        self.x += 50 * dt  # 50 pixels per second

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", (self.x, 300), 40)


if __name__ == "__main__":
    App(MovingCircle(), size=(800, 600), title="Moving circle").run()
```

`update` is called with a fixed `dt` whatever the frame rate, so simulations
behave the same on fast and slow machines. `draw` receives a screen that has
already been cleared, and should only draw.

### Controls

Every simulation run by `App` gets these keys:

| Key | Action |
|---|---|
| Esc | Quit |
| Space | Pause or resume |
| . (period) | While paused, advance by one step |
| F | Toggle fullscreen |

All other events are passed to `Simulation.handle_event`. The window title
shows the frame rate and whether the simulation is paused.

## Design

- **Simulation logic is separate from drawing.** A `Simulation` holds state
  and updates it without a window, so it can be tested with pytest.
- **Fixed time step.** `FixedStep` turns irregular frame times into a whole
  number of equal updates. Frame times are clamped so that one slow frame
  can't trigger an ever-growing backlog of updates.
- **NumPy arrays** for large numbers of agents, particles and cells.
- **Seeded randomness.** Components take a `numpy.random.Generator` instead
  of using global random state, so runs can be reproduced.

## Project layout

```
simlib/
    core/
        app.py       Simulation base class and App (window, loop, keys)
        timing.py    FixedStep fixed time step
examples/            one runnable script per component
tests/               pytest tests
```

## Running the tests

```bash
pytest
```

## Roadmap

1. **Foundations:** application framework (done), vector utilities, array
   renderer and colour palettes, seeded random generator and configuration
   loading, then port boids and an ant colony simulation onto the framework.
2. **Interaction and performance:** UI widgets, live graphs, a spatial hash
   grid, and steering behaviours extracted from boids.
3. **Grids and fields:** a cellular automaton framework, falling sand,
   reaction-diffusion, and a model of visual hallucination patterns in V1.
4. **Evolution and learning:** a from-scratch neural network with genome
   encoding and a genetic algorithm.
5. **Physics, graphs and procedural generation:** integrators, particles and
   constraints, network malware spread (SIR model), pathfinding, mazes,
   noise and L-systems.
6. **Polish:** documentation, demo GIFs and a recording utility.

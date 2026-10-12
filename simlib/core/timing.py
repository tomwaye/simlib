
class FixedStep:
    """Turns irregular frame times into a whole number of fixed-size steps."""

    def __init__(self, step: float, max_frame_time: float = 0.25) -> None:
        """Create a stepper.

        Args:
            step: Length of one simulation step in seconds. Must be positive.
            max_frame_time: Longest frame time, in seconds, that advance will
                accept. Longer frames are clamped to this, which stops a long
                hitch from triggering a burst of catch-up updates (the
                "spiral of death"). Must be positive.

        Raises:
            ValueError: If step or max_frame_time is not positive.
        """
        if step <= 0:
            raise ValueError(f"step must be positive, got {step}")
        if max_frame_time <= 0:
            raise ValueError(f"max_frame_time must be positive, got {max_frame_time}")
        self.step = step
        self.max_frame_time = max_frame_time
        self._accumulator = 0.0

    def advance(self, frame_time: float) -> int:
        """Add frame_time seconds and return how many steps to run now.

        Negative frame times are treated as 0, since a clock can occasionally
        report a tiny backwards jump. Frame times above max_frame_time are
        clamped to it. Leftover time smaller than one step carries over to
        the next call.
        """
        frame_time = min(max(0.0, frame_time), self.max_frame_time)
        self._accumulator += frame_time
        updates_to_run = 0
        while self._accumulator >= self.step:
            self._accumulator -= self.step
            updates_to_run += 1
        return updates_to_run

    @property
    def alpha(self) -> float:
        """Leftover time as a fraction of one step, in [0, 1).

        Useful for interpolating drawing between the previous and current
        simulation states.
        """
        return self._accumulator / self.step

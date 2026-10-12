import pytest

from simlib.core.timing import FixedStep

STEP = 1 / 60


def test_exact_step_runs_one_update():
    stepper = FixedStep(STEP)
    assert stepper.advance(STEP) == 1


def test_short_frame_runs_no_updates():
    stepper = FixedStep(STEP)
    assert stepper.advance(0.010) == 0


def test_leftover_carries_between_calls():
    # The 10 ms -> 25 ms rows from the worked table: 0 updates, then 2.
    stepper = FixedStep(STEP)
    assert stepper.advance(0.010) == 0
    assert stepper.advance(0.025) == 2


def test_long_frame_is_clamped():
    clamped = FixedStep(STEP, max_frame_time=0.25)
    reference = FixedStep(STEP, max_frame_time=0.25)
    assert clamped.advance(600) == reference.advance(0.25)


def test_negative_frame_time_is_treated_as_zero():
    stepper = FixedStep(STEP)
    assert stepper.advance(-1) == 0
    assert stepper.alpha == 0
    # The bad frame must not delay later updates.
    assert stepper.advance(STEP) == 1


def test_alpha_stays_in_range():
    stepper = FixedStep(STEP)
    for frame_time in [0.003, 0.010, 0.025, 0.016, 0.050, 0.1]:
        stepper.advance(frame_time)
        assert 0 <= stepper.alpha < 1


@pytest.mark.parametrize("step", [0, -0.1])
def test_non_positive_step_raises(step):
    with pytest.raises(ValueError):
        FixedStep(step)


@pytest.mark.parametrize("max_frame_time", [0, -1])
def test_non_positive_max_frame_time_raises(max_frame_time):
    with pytest.raises(ValueError):
        FixedStep(STEP, max_frame_time=max_frame_time)

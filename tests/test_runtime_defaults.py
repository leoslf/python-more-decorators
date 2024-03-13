import pytest

from unittest.mock import Mock

from datetime import datetime
from freezegun import freeze_time

from more_decorators.runtime_defaults import RuntimeDefault, evaluate_runtime_defaults, runtime_default

# NOTE: it has to be a indirection here to allow patching
now = Mock(side_effect=lambda: datetime.now())

class Dummy:
    @evaluate_runtime_defaults
    def dummy(self, time: datetime = runtime_default(now)) -> datetime:
        return time

@evaluate_runtime_defaults
def dummy(time: datetime = runtime_default(now)) -> datetime:
    return time

@pytest.mark.parametrize("function", [Dummy().dummy, dummy])
def test_evaluate_default_factory_called_once_upon_function_call(function):
    with freeze_time("1970-01-01T00:00:00.000+00:00") as frozen_datetime:
        now.reset_mock()
        actual = function()
        assert not isinstance(actual, RuntimeDefault), "The default parameter should have been evaluated"
        assert actual == frozen_datetime(), "The default parameter should be the same as the datetime.now() at the frozen moment"
        assert now.call_count == 1, "The default factory should be called only once"

        now.reset_mock()
        # increment the time to show that the default argument is freshly retrieved from the default factory
        frozen_datetime.tick()
        actual = function()
        assert not isinstance(actual, RuntimeDefault), "The default parameter should have been evaluated"
        assert actual == frozen_datetime(), "The default parameter should be the same as the datetime.now() at the frozen moment"
        assert now.call_count == 1, "The default factory should be called only once"

@pytest.mark.parametrize("function", [Dummy().dummy, dummy])
def test_evaluate_default_factory_still_accept_passed_in_argument(function):
    now.reset_mock()
    expected = datetime.fromisoformat("2024-03-12T13:18:00.000-04:00")
    assert function(expected) == expected
    assert now.call_count == 0

def test_runtime_default_should_raise_ValueError_if_factory_not_callable():
    with pytest.raises(ValueError):
        runtime_default(0)

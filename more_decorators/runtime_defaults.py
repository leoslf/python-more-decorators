from typing import TypeVar, ParamSpec, Generic, Callable
from functools import wraps
from inspect import signature
from dataclasses import dataclass

T = TypeVar("T")
V = TypeVar("V")
P = ParamSpec("P")

@dataclass
class RuntimeDefault(Generic[T]):
    __match_args__ = ("default_factory",)

    default_factory: Callable[[], T]

def runtime_default(default_factory: Callable[[], T]) -> T:
    # HACK: bypass static type checking and claim the return type is T
    if not callable(default_factory):
        raise ValueError(f"{default_factory} is not callable")
    return RuntimeDefault(default_factory) # type: ignore


def evaluate_runtime_defaults(original_function: Callable[P, T]) -> Callable[P, T]:
    def evaluate(value: V | RuntimeDefault[V]) -> V:
        match value:
            case RuntimeDefault(default_factory):
                return default_factory()
            case _:
                return value

    @wraps(original_function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        binding = signature(original_function).bind(*args, **kwargs)
        binding.apply_defaults()
        # apply evaluated arguments
        return original_function(**{ key: evaluate(value) for key, value in binding.arguments.items() })

    return wrapper

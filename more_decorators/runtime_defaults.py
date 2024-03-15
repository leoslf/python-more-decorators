from typing import TypeVar, ParamSpec, Generic, Callable, cast
from functools import wraps
from inspect import signature
from dataclasses import dataclass

__all__ = ["runtime_default", "evaluate_runtime_defaults"]

# TODO: consider using PEP695 generics to get rid of global type variables
T = TypeVar("T")
V = TypeVar("V")
P = ParamSpec("P")

@dataclass
class RuntimeDefault(Generic[T]):
    """ Runtime default argument wrapper
    Only exists before @evaluate_runtime_defaults
    """
    __match_args__ = ("default_factory",)

    default_factory: Callable[[], T]

def runtime_default(default_factory: Callable[[], T]) -> T:
    """ Runtime-default argument declaration

    Wraps the default_factory into a temporary wrapper and defer the evaluation to :func:`~evaluate_runtime_defaults`.
    
    Args:
        default_factory: A :abbr:`nullary (taking no arguments)` function to be lazily-evaluated upon function call to produce the desired default value.  Useful for mutable type defaults or immutable types involving side-effects (e.g. :func:`time.time`, :class:`datetime.datetime`).
    
    Returns:
        The wrapper containing the default_factory to be evaluated, casted to type T to make type checker happy
    """
    if not callable(default_factory):
        raise ValueError(f"{default_factory} is not callable")

    # HACK: bypass static type checking and claim the return type is T
    return cast(T, RuntimeDefault(default_factory))


def evaluate_runtime_defaults(original_function: Callable[P, T]) -> Callable[P, T]:
    """ Evaluator of runtime-default arguments

    Args:
        original_function: The function to be decorated

    Returns:
        The decorated function that will have its runtime-default arguments evaluated upon function call
    """
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

# Python More Decorators

Python More Decorators is a handy library to simplify your code with a collection of useful decorators.

- Works with type checking (tested with `mypy`)

## Installation

### pip

```bash
pip install python-more-decorators
```

### poetry

```bash
poetry add python-more-decorators
```

## Features

### Evaluate runtime-default arguments

Sometimes we are just tired of polluting the function arguments declaration with `None` as `argument: Optional[MutableType] = None`.
Or, we have all been here: having `some_list_argument: list[T] = []` or `now: float = time.time()` in arguments.

The worst thing is that it still runs.

We now have:

```python
from more_decorators.runtime_defaults import evaluate_runtime_defaults, runtime_default

@evaluate_runtime_defaults
def foo(now: float = runtime_default(time.time)): # think of it like `now: float = time.time()`
                                                  # but evaluated every time upon function call
    return f"Unix Timestamp: {now}"
```

...and more to come.

## License

This library is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md)


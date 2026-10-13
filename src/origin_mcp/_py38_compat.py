"""Local compatibility for Origin 2021's embedded Python 3.8."""

import builtins
import itertools


def zip_compat(*iterables, strict=False):
    if not strict:
        yield from builtins.zip(*iterables)  # noqa: B905 -- Python 3.8 has no strict keyword.
        return
    sentinel = object()
    for values in itertools.zip_longest(*iterables, fillvalue=sentinel):
        if any(value is sentinel for value in values):
            raise ValueError("zip() arguments have different lengths")
        yield values

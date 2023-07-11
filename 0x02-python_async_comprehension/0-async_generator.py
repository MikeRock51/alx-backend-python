#!/usr/bin/env python3
"""
    Write a coroutine called async_generator that takes no arguments.
    The coroutine will loop 10 times, each time asynchronously wait
    1 second, then yield a random number between 0 and 10.
"""


import asyncio
from random import uniform
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Asynchronously yields a random number between 0 and 10, 10 times"""

    for _ in range(10):
        rand = uniform(0, 10)
        await asyncio.sleep(1)
        yield rand

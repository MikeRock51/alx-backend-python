#!/usr/bin/env python3
"""Execute multiple coroutines at the same time with async"""

import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> list:
    delays = []

    delays.append(await asyncio.gather(*(wait_random(max_delay) for i in range(n))))
    return delays

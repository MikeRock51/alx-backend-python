#!/usr/bin/env python3
"""The basics of async"""


import asyncio
import random


async def wait_random(max_delay: int = 10):
    delay = random.uniform(0, max_delay)
    asyncio.sleep(delay)
    return delay

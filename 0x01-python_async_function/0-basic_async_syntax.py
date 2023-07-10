#!/usr/bin/env python3
"""The basics of async"""


import asyncio
import random


async def wait_random(max_delay: int = 10):
    """Returns a random number between 0 and max_delay"""
    delay = random.uniform(0, max_delay + 1e-10)
    asyncio.sleep(delay)
    return delay

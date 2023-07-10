#!/usr/bin/env python3
"""Execute multiple coroutines at the same time with async"""

import asyncio
from typing import List
import heapq


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Returns a sorted list of delays"""

    delays = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))
    heapq.heapify(delays)

    sortedDelays = [heapq.heappop(delays) for _ in range(n)]

    return sortedDelays

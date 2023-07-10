#!/usr/bin/env python3
"""Execute multiple coroutines at the same time with async"""

import asyncio
from typing import List
import heapq


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Returns a sorted list of delays"""

    delays = await asyncio.gather(*(task_wait_random(max_delay)
                                    for _ in range(n)))

    heapq.heapify(delays)
    sortedDelays = [heapq.heappop(delays) for _ in range(n)]

    return sortedDelays

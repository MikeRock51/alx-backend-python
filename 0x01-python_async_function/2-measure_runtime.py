#!/usr/bin/env python3
"""Measuring run time"""

import time
import asyncio


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Measures the total execution time of wait_n"""

    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end = time.perf_counter() - start

    return end / n

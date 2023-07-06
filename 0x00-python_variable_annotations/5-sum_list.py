#!/usr/bin/env python3
"""
    Defines a type-annotated function sum_list which takes a list
    input_list of floats as argument and returns their sum as a float.
"""

from typing import List


def sum_list(input_list: List[float]) -> float:
    """Returns the sum of input_list"""

    return sum(input_list)

#!/usr/bin/env python3

from typing import Mapping
from parameterized import parameterized
from nose.tools import assert_equal


nested_map = {"a": {"b": {"c": 1}}}
path = ['a', 'b', 'c']

for key in path:
    if not isinstance(nested_map, Mapping):
        raise KeyError(key)
    nested_map = nested_map[key]
    # print(nested_map)
    
print(nested_map)

def pray(first, second, third):
    return first + second

@parameterized.expand([(2, 2, 4)])
def test_pray(first, second, third):
    prayer = pray(first, second, third)
    assert_equal(prayer, 5)
    print(f"{first} + {second} = {third}")


if __name__ == '__main__':
    test_pray()
    print("Done")

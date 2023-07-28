#!/usr/bin/env python3

from typing import Mapping

nested_map = {"a": {"b": {"c": 1}}}
path = ['a', 'b', 'c']

for key in path:
    if not isinstance(nested_map, Mapping):
        raise KeyError(key)
    nested_map = nested_map[key]
    # print(nested_map)
    
print(nested_map)

#!/usr/bin/env python
"""
quick sort algrithm, almost by copilot
"""


def quick_sort(lst: list):
    if len(lst) <= 1:
        return lst
    pivot = lst[0]
    left = [x for x in lst[1:] if x <= pivot]
    right = [x for x in lst[1:] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)


def quick_sort_non_recursive(lst: list):
    if len(lst) <= 1:
        return lst
    stack = [lst]
    result = []
    while stack:
        lst = stack.pop()
        if len(lst) <= 1:
            result.extend(lst)
            continue
        pivot = lst[0]
        left = [x for x in lst[1:] if x <= pivot]
        right = [x for x in lst[1:] if x > pivot]
        stack.append(right)
        stack.append([pivot])
        stack.append(left)
    return result


def test_quicksort():
    import random
    lst = [random.randint(0, 100) for _ in range(100)]
    assert quick_sort(lst) == sorted(lst)
    res = quick_sort_non_recursive(lst)
    assert res == sorted(lst), (res, lst)

def test_quicksort2():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert quick_sort(lst) == sorted(lst)
    res = quick_sort_non_recursive(lst)
    assert res == sorted(lst), (res, lst)

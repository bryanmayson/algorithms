"""
 Basic bSearch algorithms
"""


def binary_search_index(my_list,key):
    """
    binary_search implementation which returns index
    
    Bryan Mayson
    """
    lo = 0
    hi = len(my_list)
    while lo < hi-1:
        mid = (lo+hi)//2
        if my_list[mid] > key:
            hi = mid
        else:
            lo = mid
    return lo

def binary_search_check(my_list,key):
    lo = 0
    hi = len(my_list)
    while lo < hi -1:
        mid = (lo+hi)//2
        if my_list[mid] == key:
            return True
        elif my_list[mid] > key:
            hi = mid
        else:
            lo = mid
    return False

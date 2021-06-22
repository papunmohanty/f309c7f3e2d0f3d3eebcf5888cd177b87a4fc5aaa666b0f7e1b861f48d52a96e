from itertools import combinations
import sys
from typing import List


def parameters_validations(_list: List[int], size: int) -> ValueError or None:
    """
    This function use to validate input parameters
    """
    list_length = len(_list)
    if not 1 <= list_length <= 20:
        raise ValueError("The input list parameter should be between 1 and 20, the actual length is {list_length}")  # noqa: E501
    if not all(map(lambda number: 1 <= number <= 1000, _list)):
        raise ValueError("Each element of a list must be in between 1 and 1000")  # noqa: E501
    if not 1 <= size <= list_length:
        raise ValueError(f"The size must be between 1 and {list_length}, given size: {size}")  # noqa: E501
    return


def non_empty_subsequence(_list: List[int], size: int) -> int:
    """
    The function returns non-empty subsequence of `_list` of size `size`
    :param _size: List
    :param size: int
    :return: int
    """
    # Checks all constraints for the input parameters
    try:
        _ = parameters_validations(_list, size)
    except Exception as err:
        print(f"Input validation exception occurred: {err}")
        sys.exit(1)

    combination = combinations(_list, size)
    return len(list(filter(
                lambda x: x <= 1000, [sum(c) for c in list(combination)]
            )
        )
    )


if __name__ == "__main__":
    print(non_empty_subsequence([1, 2, 8], 2))
    print(non_empty_subsequence([5, 17, 1000, 11], 4))
    # Invalid cases, un-comment one by one to test the
    # functionality of `non_empty_subsequence` function
    # print(non_empty_subsequence([1, 0, 13], 2))
    # print(non_empty_subsequence([1, -1, 13], 2))
    # print(non_empty_subsequence([1001, 2, 1], 2))
    # print(non_empty_subsequence([1000, 2, 1], 20))
    # print(non_empty_subsequence([1000, 2, 1, 2, 34, 45, 54, 56, 88, 12, 34, 45, 1, 11, 111, 222, 333, 444, 555, 666], 21))  # noqa: E501
